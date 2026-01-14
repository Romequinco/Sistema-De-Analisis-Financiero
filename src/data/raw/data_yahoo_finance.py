"""
Módulo de extracción de datos financieros usando Yahoo Finance (yfinance).

Este módulo proporciona una interfaz unificada para obtener datos de mercado
de acciones, ETFs, criptomonedas y otros activos financieros a través de
Yahoo Finance como proveedor de datos.

Implementación específica para Yahoo Finance. Para usar otros proveedores,
crear módulos similares (ej: data_alpha_vantage.py, data_polygon.py).
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import pickle
import json
from typing import Optional, Dict, List, Union
import logging
import time

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProvider:
    """
    Proveedor de datos financieros usando yfinance.
    
    Características:
    - Cache local para evitar llamadas innecesarias
    - Soporte para múltiples tipos de activos
    - Normalización de datos
    - Manejo de errores robusto
    """
    
    def __init__(self, cache_dir: Optional[Path] = None, timeout: int = 60, max_retries: int = 3):
        """
        Inicializa el proveedor de datos.
        
        Args:
            cache_dir: Directorio para almacenar cache. Por defecto: data/raw/
            timeout: Timeout en segundos para las peticiones (default: 60)
            max_retries: Número máximo de reintentos en caso de error (default: 3)
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent.parent.parent / "data" / "raw"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuración de cache (en horas)
        self.cache_ttl = 1  # 1 hora por defecto
        
        # Configuración de red
        self.timeout = timeout
        self.max_retries = max_retries
    
    def _get_cache_path(self, symbol: str, data_type: str) -> Path:
        """Genera la ruta del archivo de cache."""
        safe_symbol = symbol.replace(":", "_").replace("/", "_")
        return self.cache_dir / f"{safe_symbol}_{data_type}.pkl"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Verifica si el cache es válido según TTL."""
        if not cache_path.exists():
            return False
        
        cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        return cache_age < timedelta(hours=self.cache_ttl)
    
    def _save_to_cache(self, data: pd.DataFrame, cache_path: Path):
        """Guarda datos en cache."""
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(data, f)
            logger.info(f"Datos guardados en cache: {cache_path.name}")
        except Exception as e:
            logger.warning(f"Error guardando cache: {e}")
    
    def _load_from_cache(self, cache_path: Path) -> Optional[pd.DataFrame]:
        """Carga datos desde cache."""
        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
            logger.info(f"Datos cargados desde cache: {cache_path.name}")
            return data
        except Exception as e:
            logger.warning(f"Error cargando cache: {e}")
            return None
    
    def get_price_data(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d",
        use_cache: bool = True
    ) -> pd.DataFrame:
        """
        Obtiene datos de precios históricos.
        
        Args:
            symbol: Símbolo del activo (ej: "AAPL", "BTC-USD")
            period: Período de datos ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max")
            interval: Intervalo de datos ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
            use_cache: Si usar cache local
        
        Returns:
            DataFrame con columnas: Open, High, Low, Close, Volume, Dividends, Stock Splits
        """
        cache_path = self._get_cache_path(symbol, f"price_{period}_{interval}")
        
        # Intentar cargar desde cache
        if use_cache and self._is_cache_valid(cache_path):
            cached_data = self._load_from_cache(cache_path)
            if cached_data is not None:
                return cached_data
        
        # Intentar cargar cache antiguo si existe (aunque haya expirado)
        if use_cache and cache_path.exists():
            logger.warning(f"Cache expirado encontrado para {symbol}. Intentando usar datos antiguos...")
            cached_data = self._load_from_cache(cache_path)
            if cached_data is not None and not cached_data.empty:
                logger.info(f"Usando datos de cache expirado para {symbol}")
                return cached_data
        
        # Descargar datos con reintentos
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Descargando datos de precios para {symbol} (intento {attempt}/{self.max_retries})...")
                ticker = yf.Ticker(symbol)
                
                # Configurar timeout más largo para yfinance
                data = ticker.history(period=period, interval=interval, timeout=self.timeout)
                
                if data.empty:
                    raise ValueError(f"No se encontraron datos para {symbol}")
                
                # Normalizar nombres de columnas
                data.columns = [col.capitalize() for col in data.columns]
                
                # Guardar en cache
                if use_cache:
                    self._save_to_cache(data, cache_path)
                
                logger.info(f"Datos descargados exitosamente para {symbol}")
                return data
                
            except Exception as e:
                last_error = e
                logger.warning(f"Intento {attempt} fallido para {symbol}: {e}")
                
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Backoff exponencial
                    logger.info(f"Reintentando en {wait_time} segundos...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Todos los intentos fallaron para {symbol}")
        
        # Si todos los intentos fallaron, intentar usar cache antiguo o lanzar error
        if use_cache and cache_path.exists():
            logger.warning(f"Usando datos de cache antiguo debido a error de red para {symbol}")
            cached_data = self._load_from_cache(cache_path)
            if cached_data is not None and not cached_data.empty:
                return cached_data
        
        raise ConnectionError(f"Error obteniendo datos de precios para {symbol} después de {self.max_retries} intentos: {last_error}")
    
    def get_fundamental_data(self, symbol: str, use_cache: bool = True) -> Dict:
        """
        Obtiene datos fundamentales del activo.
        
        Args:
            symbol: Símbolo del activo
            use_cache: Si usar cache local
        
        Returns:
            Diccionario con información fundamental
        """
        cache_path = self._get_cache_path(symbol, "fundamental")
        
        # Intentar cargar desde cache
        if use_cache and self._is_cache_valid(cache_path):
            cached_data = self._load_from_cache(cache_path)
            if cached_data is not None:
                return cached_data
        
        # Intentar cargar cache antiguo si existe
        if use_cache and cache_path.exists():
            logger.warning(f"Cache expirado encontrado para fundamentales de {symbol}. Intentando usar datos antiguos...")
            cached_data = self._load_from_cache(cache_path)
            if cached_data is not None:
                logger.info(f"Usando datos de cache expirado para fundamentales de {symbol}")
                return cached_data
        
        # Descargar datos con reintentos
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Descargando datos fundamentales para {symbol} (intento {attempt}/{self.max_retries})...")
                ticker = yf.Ticker(symbol)
                
                info = ticker.info
                
                # Extraer información relevante
                fundamental_data = {
                    "symbol": symbol,
                    "name": info.get("longName", info.get("shortName", "")),
                    "sector": info.get("sector", ""),
                    "industry": info.get("industry", ""),
                    "market_cap": info.get("marketCap"),
                    "enterprise_value": info.get("enterpriseValue"),
                    "pe_ratio": info.get("trailingPE"),
                    "forward_pe": info.get("forwardPE"),
                    "peg_ratio": info.get("pegRatio"),
                    "price_to_book": info.get("priceToBook"),
                    "price_to_sales": info.get("priceToSalesTrailing12Months"),
                    "dividend_yield": info.get("dividendYield"),
                    "payout_ratio": info.get("payoutRatio"),
                    "revenue_growth": info.get("revenueGrowth"),
                    "earnings_growth": info.get("earningsGrowth"),
                    "profit_margin": info.get("profitMargins"),
                    "operating_margin": info.get("operatingMargins"),
                    "roe": info.get("returnOnEquity"),
                    "roa": info.get("returnOnAssets"),
                    "debt_to_equity": info.get("debtToEquity"),
                    "current_ratio": info.get("currentRatio"),
                    "quick_ratio": info.get("quickRatio"),
                    "beta": info.get("beta"),
                    "52_week_high": info.get("fiftyTwoWeekHigh"),
                    "52_week_low": info.get("fiftyTwoWeekLow"),
                    "current_price": info.get("currentPrice"),
                    "target_price": info.get("targetMeanPrice"),
                    "recommendation": info.get("recommendationKey", "").upper(),
                    "number_of_analysts": info.get("numberOfAnalystOpinions"),
                }
                
                # Guardar en cache
                if use_cache:
                    self._save_to_cache(fundamental_data, cache_path)
                
                logger.info(f"Datos fundamentales descargados exitosamente para {symbol}")
                return fundamental_data
                
            except Exception as e:
                last_error = e
                logger.warning(f"Intento {attempt} fallido para fundamentales de {symbol}: {e}")
                
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt  # Backoff exponencial
                    logger.info(f"Reintentando en {wait_time} segundos...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Todos los intentos fallaron para fundamentales de {symbol}")
        
        # Si todos los intentos fallaron, intentar usar cache antiguo o lanzar error
        if use_cache and cache_path.exists():
            logger.warning(f"Usando datos de cache antiguo debido a error de red para fundamentales de {symbol}")
            cached_data = self._load_from_cache(cache_path)
            if cached_data is not None:
                return cached_data
        
        raise ConnectionError(f"Error obteniendo datos fundamentales para {symbol} después de {self.max_retries} intentos: {last_error}")
    
    def get_financial_statements(
        self,
        symbol: str,
        statement_type: str = "income",
        use_cache: bool = True
    ) -> pd.DataFrame:
        """
        Obtiene estados financieros.
        
        Args:
            symbol: Símbolo del activo
            statement_type: Tipo de estado ("income", "balance", "cashflow")
            use_cache: Si usar cache local
        
        Returns:
            DataFrame con el estado financiero
        """
        cache_path = self._get_cache_path(symbol, f"statement_{statement_type}")
        
        # Intentar cargar desde cache
        if use_cache and self._is_cache_valid(cache_path):
            cached_data = self._load_from_cache(cache_path)
            if cached_data is not None:
                return cached_data
        
        try:
            logger.info(f"Descargando {statement_type} statement para {symbol}...")
            ticker = yf.Ticker(symbol)
            
            if statement_type == "income":
                data = ticker.financials
            elif statement_type == "balance":
                data = ticker.balance_sheet
            elif statement_type == "cashflow":
                data = ticker.cashflow
            else:
                raise ValueError(f"Tipo de estado no válido: {statement_type}")
            
            if data.empty:
                raise ValueError(f"No se encontraron datos de {statement_type} para {symbol}")
            
            # Guardar en cache
            if use_cache:
                self._save_to_cache(data, cache_path)
            
            return data
            
        except Exception as e:
            logger.error(f"Error obteniendo {statement_type} statement para {symbol}: {e}")
            raise
    
    def get_all_data(
        self,
        symbol: str,
        period: str = "1y",
        use_cache: bool = True
    ) -> Dict[str, Union[pd.DataFrame, Dict]]:
        """
        Obtiene todos los datos disponibles para un símbolo.
        
        Args:
            symbol: Símbolo del activo
            period: Período para datos de precios
            use_cache: Si usar cache local
        
        Returns:
            Diccionario con todos los datos
        """
        return {
            "price_data": self.get_price_data(symbol, period=period, use_cache=use_cache),
            "fundamental_data": self.get_fundamental_data(symbol, use_cache=use_cache),
            "income_statement": self.get_financial_statements(symbol, "income", use_cache=use_cache),
            "balance_sheet": self.get_financial_statements(symbol, "balance", use_cache=use_cache),
            "cashflow_statement": self.get_financial_statements(symbol, "cashflow", use_cache=use_cache),
        }
    
    def clear_cache(self, symbol: Optional[str] = None):
        """
        Limpia el cache.
        
        Args:
            symbol: Si se especifica, solo limpia cache de ese símbolo. Si es None, limpia todo.
        """
        if symbol:
            pattern = symbol.replace(":", "_").replace("/", "_")
            cache_files = list(self.cache_dir.glob(f"{pattern}*"))
        else:
            cache_files = list(self.cache_dir.glob("*.pkl"))
        
        for cache_file in cache_files:
            try:
                cache_file.unlink()
                logger.info(f"Cache eliminado: {cache_file.name}")
            except Exception as e:
                logger.warning(f"Error eliminando cache {cache_file.name}: {e}")


# Funciones de utilidad para visualización
def format_number(value: Union[float, int]) -> str:
    """
    Formatea números grandes en formato legible (B, M, K).
    
    Args:
        value: Valor numérico a formatear
    
    Returns:
        String formateado
    """
    if pd.isna(value) or value == 0:
        return 'N/A'
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"


def create_fundamental_tables(fundamental_data: Dict) -> Dict[str, pd.DataFrame]:
    """
    Crea DataFrames organizados por categorías para datos fundamentales.
    
    Args:
        fundamental_data: Diccionario con datos fundamentales
    
    Returns:
        Diccionario con DataFrames por categoría
    """
    tables = {}
    
    # Tabla 1: Información General
    general_data = {
        'Métrica': ['Nombre', 'Sector', 'Industria'],
        'Valor': [
            fundamental_data.get('name', 'N/A'),
            fundamental_data.get('sector', 'N/A'),
            fundamental_data.get('industry', 'N/A')
        ]
    }
    tables['general'] = pd.DataFrame(general_data)
    
    # Tabla 2: Valoración
    valuation_data = {
        'Métrica': [
            'Market Cap',
            'Enterprise Value',
            'PE Ratio',
            'Forward PE',
            'PEG Ratio',
            'Price to Book',
            'Price to Sales',
            'Dividend Yield',
            'Payout Ratio'
        ],
        'Valor': [
            f"${fundamental_data.get('market_cap', 0):,.0f}" if fundamental_data.get('market_cap') is not None else 'N/A',
            f"${fundamental_data.get('enterprise_value', 0):,.0f}" if fundamental_data.get('enterprise_value') is not None else 'N/A',
            f"{fundamental_data.get('pe_ratio', 0):.2f}" if fundamental_data.get('pe_ratio') is not None else 'N/A',
            f"{fundamental_data.get('forward_pe', 0):.2f}" if fundamental_data.get('forward_pe') is not None else 'N/A',
            f"{fundamental_data.get('peg_ratio', 0):.2f}" if fundamental_data.get('peg_ratio') is not None else 'N/A',
            f"{fundamental_data.get('price_to_book', 0):.2f}" if fundamental_data.get('price_to_book') is not None else 'N/A',
            f"{fundamental_data.get('price_to_sales', 0):.2f}" if fundamental_data.get('price_to_sales') is not None else 'N/A',
            f"{fundamental_data.get('dividend_yield', 0)*100:.2f}%" if fundamental_data.get('dividend_yield') is not None else 'N/A',
            f"{fundamental_data.get('payout_ratio', 0)*100:.2f}%" if fundamental_data.get('payout_ratio') is not None else 'N/A'
        ]
    }
    tables['valuation'] = pd.DataFrame(valuation_data)
    
    # Tabla 3: Rentabilidad
    profitability_data = {
        'Métrica': [
            'ROE (Return on Equity)',
            'ROA (Return on Assets)',
            'Profit Margin',
            'Operating Margin'
        ],
        'Valor': [
            f"{fundamental_data.get('roe', 0)*100:.2f}%" if fundamental_data.get('roe') is not None else 'N/A',
            f"{fundamental_data.get('roa', 0)*100:.2f}%" if fundamental_data.get('roa') is not None else 'N/A',
            f"{fundamental_data.get('profit_margin', 0)*100:.2f}%" if fundamental_data.get('profit_margin') is not None else 'N/A',
            f"{fundamental_data.get('operating_margin', 0)*100:.2f}%" if fundamental_data.get('operating_margin') is not None else 'N/A'
        ]
    }
    tables['profitability'] = pd.DataFrame(profitability_data)
    
    # Tabla 4: Crecimiento
    growth_data = {
        'Métrica': [
            'Revenue Growth',
            'Earnings Growth'
        ],
        'Valor': [
            f"{fundamental_data.get('revenue_growth', 0)*100:.2f}%" if fundamental_data.get('revenue_growth') is not None else 'N/A',
            f"{fundamental_data.get('earnings_growth', 0)*100:.2f}%" if fundamental_data.get('earnings_growth') is not None else 'N/A'
        ]
    }
    tables['growth'] = pd.DataFrame(growth_data)
    
    # Tabla 5: Salud Financiera
    health_data = {
        'Métrica': [
            'Debt to Equity',
            'Current Ratio',
            'Quick Ratio',
            'Beta'
        ],
        'Valor': [
            f"{fundamental_data.get('debt_to_equity', 0):.2f}" if fundamental_data.get('debt_to_equity') is not None else 'N/A',
            f"{fundamental_data.get('current_ratio', 0):.2f}" if fundamental_data.get('current_ratio') is not None else 'N/A',
            f"{fundamental_data.get('quick_ratio', 0):.2f}" if fundamental_data.get('quick_ratio') is not None else 'N/A',
            f"{fundamental_data.get('beta', 0):.2f}" if fundamental_data.get('beta') is not None else 'N/A'
        ]
    }
    tables['health'] = pd.DataFrame(health_data)
    
    # Tabla 6: Precios y Recomendaciones
    price_data_table = {
        'Métrica': [
            'Precio Actual',
            '52 Week High',
            '52 Week Low',
            'Target Price',
            'Recomendación',
            'Número de Analistas'
        ],
        'Valor': [
            f"${fundamental_data.get('current_price', 0):.2f}" if fundamental_data.get('current_price') is not None else 'N/A',
            f"${fundamental_data.get('52_week_high', 0):.2f}" if fundamental_data.get('52_week_high') is not None else 'N/A',
            f"${fundamental_data.get('52_week_low', 0):.2f}" if fundamental_data.get('52_week_low') is not None else 'N/A',
            f"${fundamental_data.get('target_price', 0):.2f}" if fundamental_data.get('target_price') is not None else 'N/A',
            fundamental_data.get('recommendation', 'N/A') or 'N/A',
            f"{fundamental_data.get('number_of_analysts', 0)}" if fundamental_data.get('number_of_analysts') is not None else 'N/A'
        ]
    }
    tables['prices'] = pd.DataFrame(price_data_table)
    
    return tables


def create_historical_tables(
    income_statement: pd.DataFrame,
    balance_sheet: pd.DataFrame,
    cashflow_statement: pd.DataFrame,
    max_years: int = 5
) -> Dict[str, pd.DataFrame]:
    """
    Crea tablas con evolución histórica de métricas financieras.
    
    Args:
        income_statement: DataFrame con estado de resultados
        balance_sheet: DataFrame con balance general
        cashflow_statement: DataFrame con flujo de efectivo
        max_years: Número máximo de años a mostrar
    
    Returns:
        Diccionario con DataFrames históricos por categoría
    """
    tables = {}
    
    # Obtener las últimas N columnas (años) disponibles
    max_cols = min(max_years, income_statement.shape[1])
    years = income_statement.columns[:max_cols]
    
    # Tabla 1: Ingresos y Beneficios
    income_metrics = {
        'Total Revenue': 'Total Revenue',
        'Cost of Revenue': 'Cost Of Revenue',
        'Gross Profit': 'Gross Profit',
        'Operating Income': 'Operating Income',
        'Net Income': 'Net Income',
        'EBITDA': 'EBITDA'
    }
    
    income_history = {}
    for metric_name, metric_key in income_metrics.items():
        if metric_key in income_statement.index:
            values = []
            for year in years:
                val = income_statement.loc[metric_key, year]
                values.append(format_number(val) if not pd.isna(val) else 'N/A')
            income_history[metric_name] = values
    
    if income_history:
        tables['income_history'] = pd.DataFrame(income_history, index=[str(y)[:4] for y in years])
    
    # Tabla 2: Balance General
    balance_metrics = {
        'Total Assets': 'Total Assets',
        'Total Liabilities': 'Total Liab',
        'Total Stockholder Equity': 'Stockholders Equity',
        'Cash And Cash Equivalents': 'Cash And Cash Equivalents',
        'Total Debt': 'Total Debt',
        'Current Assets': 'Current Assets',
        'Current Liabilities': 'Current Liabilities'
    }
    
    balance_history = {}
    for metric_name, metric_key in balance_metrics.items():
        if metric_key in balance_sheet.index:
            values = []
            for year in years:
                val = balance_sheet.loc[metric_key, year]
                values.append(format_number(val) if not pd.isna(val) else 'N/A')
            balance_history[metric_name] = values
    
    if balance_history:
        tables['balance_history'] = pd.DataFrame(balance_history, index=[str(y)[:4] for y in years])
    
    # Tabla 3: Flujo de Efectivo
    cashflow_metrics = {
        'Operating Cash Flow': 'Total Cash From Operating Activities',
        'Capital Expenditure': 'Capital Expenditures',
        'Dividends Paid': 'Dividends Paid',
        'Net Borrowings': 'Net Borrowings'
    }
    
    cashflow_history = {}
    for metric_name, metric_key in cashflow_metrics.items():
        if metric_key in cashflow_statement.index:
            values = []
            for year in years:
                val = cashflow_statement.loc[metric_key, year]
                values.append(format_number(val) if not pd.isna(val) else 'N/A')
            cashflow_history[metric_name] = values
    
    # Calcular Free Cash Flow
    if 'Total Cash From Operating Activities' in cashflow_statement.index and 'Capital Expenditures' in cashflow_statement.index:
        fcf_values = []
        for year in years:
            operating_cf = cashflow_statement.loc['Total Cash From Operating Activities', year]
            capex = cashflow_statement.loc['Capital Expenditures', year]
            if not pd.isna(operating_cf) and not pd.isna(capex):
                fcf = operating_cf - abs(capex)  # Capex es negativo
                fcf_values.append(format_number(fcf))
            else:
                fcf_values.append('N/A')
        cashflow_history['Free Cash Flow'] = fcf_values
    
    if cashflow_history:
        tables['cashflow_history'] = pd.DataFrame(cashflow_history, index=[str(y)[:4] for y in years])
    
    # Tabla 4: Ratios Calculados Históricos
    ratios_history = {}
    
    for year in years:
        year_str = str(year)[:4]
        
        # Obtener valores del año
        revenue = income_statement.loc['Total Revenue', year] if 'Total Revenue' in income_statement.index else None
        net_income = income_statement.loc['Net Income', year] if 'Net Income' in income_statement.index else None
        total_assets = balance_sheet.loc['Total Assets', year] if 'Total Assets' in balance_sheet.index else None
        total_equity = balance_sheet.loc['Stockholders Equity', year] if 'Stockholders Equity' in balance_sheet.index else None
        total_debt = balance_sheet.loc['Total Debt', year] if 'Total Debt' in balance_sheet.index else None
        
        # Calcular ratios
        profit_margin = (net_income / revenue * 100) if revenue and net_income and revenue != 0 else None
        roa = (net_income / total_assets * 100) if net_income and total_assets and total_assets != 0 else None
        roe = (net_income / total_equity * 100) if net_income and total_equity and total_equity != 0 else None
        debt_to_equity = (total_debt / total_equity) if total_debt and total_equity and total_equity != 0 else None
        
        ratios_history[year_str] = {
            'Profit Margin (%)': f"{profit_margin:.2f}%" if profit_margin is not None else 'N/A',
            'ROA (%)': f"{roa:.2f}%" if roa is not None else 'N/A',
            'ROE (%)': f"{roe:.2f}%" if roe is not None else 'N/A',
            'Debt/Equity': f"{debt_to_equity:.2f}" if debt_to_equity is not None else 'N/A'
        }
    
    if ratios_history:
        tables['ratios_history'] = pd.DataFrame(ratios_history).T
    
    return tables


# Función de conveniencia para uso rápido
def get_data(symbol: str, period: str = "1y", use_cache: bool = True) -> Dict:
    """
    Función de conveniencia para obtener datos rápidamente.
    
    Args:
        symbol: Símbolo del activo
        period: Período para datos de precios
        use_cache: Si usar cache local
    
    Returns:
        Diccionario con todos los datos
    """
    provider = DataProvider()
    return provider.get_all_data(symbol, period=period, use_cache=use_cache)
