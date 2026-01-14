"""
Módulo de extracción de datos financieros usando yfinance.

Este módulo proporciona una interfaz unificada para obtener datos de mercado
de acciones, ETFs, criptomonedas y otros activos financieros.
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
            cache_dir = Path(__file__).parent.parent.parent / "data" / "raw"
        
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
