"""
Módulo de limpieza y preprocesamiento de datos financieros.

Este módulo se encarga de limpiar, normalizar y validar datos financieros
obtenidos de cualquier fuente, preparándolos para análisis posterior.

Filosofía:
- Separación estricta entre extracción y limpieza
- Explicabilidad sobre complejidad
- Validación robusta de datos financieros
- Metadata completa de transformaciones
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime
import logging
from dataclasses import dataclass, field
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CleaningMetadata:
    """
    Metadata sobre las transformaciones realizadas durante la limpieza.
    """
    original_shape: Tuple[int, int] = (0, 0)
    final_shape: Tuple[int, int] = (0, 0)
    rows_removed: int = 0
    columns_removed: List[str] = field(default_factory=list)
    null_values_filled: int = 0
    null_values_removed: int = 0
    duplicates_removed: int = 0
    outliers_detected: int = 0
    invalid_ohlc_rows: int = 0
    warnings: List[str] = field(default_factory=list)
    transformations_applied: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convierte la metadata a diccionario."""
        return {
            'original_shape': self.original_shape,
            'final_shape': self.final_shape,
            'rows_removed': self.rows_removed,
            'columns_removed': self.columns_removed,
            'null_values_filled': self.null_values_filled,
            'null_values_removed': self.null_values_removed,
            'duplicates_removed': self.duplicates_removed,
            'outliers_detected': self.outliers_detected,
            'invalid_ohlc_rows': self.invalid_ohlc_rows,
            'warnings': self.warnings,
            'transformations_applied': self.transformations_applied
        }
    
    def summary(self) -> str:
        """Genera un resumen legible de la limpieza."""
        lines = [
            f"Forma original: {self.original_shape}",
            f"Forma final: {self.final_shape}",
            f"Filas eliminadas: {self.rows_removed}",
            f"Columnas eliminadas: {len(self.columns_removed)}",
            f"Valores nulos imputados: {self.null_values_filled}",
            f"Valores nulos eliminados: {self.null_values_removed}",
            f"Duplicados eliminados: {self.duplicates_removed}",
            f"Outliers detectados: {self.outliers_detected}",
            f"Filas OHLC inválidas: {self.invalid_ohlc_rows}",
        ]
        
        if self.warnings:
            lines.append(f"\nAdvertencias ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"  - {warning}")
        
        if self.transformations_applied:
            lines.append(f"\nTransformaciones aplicadas:")
            for transform in self.transformations_applied:
                lines.append(f"  - {transform}")
        
        return "\n".join(lines)


class DataCleaner:
    """
    Clase principal para limpieza y preprocesamiento de datos financieros.
    
    Características:
    - Limpieza de datos de precios OHLCV
    - Limpieza de datos fundamentales
    - Limpieza de estados financieros
    - Validación robusta
    - Metadata completa de transformaciones
    """
    
    def __init__(self, 
                 fill_method: str = 'forward',
                 remove_outliers: bool = False,
                 outlier_threshold: float = 3.0,
                 validate_ohlc: bool = True,
                 normalize_column_names: bool = True):
        """
        Inicializa el DataCleaner.
        
        Args:
            fill_method: Método para llenar valores nulos ('forward', 'backward', 'interpolate', 'drop')
            remove_outliers: Si eliminar outliers automáticamente
            outlier_threshold: Desviaciones estándar para detectar outliers
            validate_ohlc: Si validar relaciones OHLC (High >= Open/Close >= Low)
            normalize_column_names: Si normalizar nombres de columnas a minúsculas
        """
        self.fill_method = fill_method
        self.remove_outliers = remove_outliers
        self.outlier_threshold = outlier_threshold
        self.validate_ohlc = validate_ohlc
        self.normalize_column_names = normalize_column_names
    
    def clean_price_data(self, 
                        data: pd.DataFrame,
                        symbol: Optional[str] = None) -> Tuple[pd.DataFrame, CleaningMetadata]:
        """
        Limpia y preprocesa datos de precios OHLCV.
        
        Args:
            data: DataFrame con datos de precios (debe tener índice datetime)
            symbol: Símbolo del activo (opcional, para logging)
        
        Returns:
            Tuple con (DataFrame limpio, CleaningMetadata)
        """
        metadata = CleaningMetadata()
        metadata.original_shape = data.shape
        
        logger.info(f"Limpiando datos de precios{' para ' + symbol if symbol else ''}...")
        
        # Crear copia para no modificar el original
        cleaned = data.copy()
        
        # 1. Normalizar nombres de columnas
        if self.normalize_column_names:
            cleaned.columns = [col.lower().strip() for col in cleaned.columns]
            metadata.transformations_applied.append("Normalización de nombres de columnas")
        
        # 2. Asegurar índice datetime
        if not isinstance(cleaned.index, pd.DatetimeIndex):
            try:
                cleaned.index = pd.to_datetime(cleaned.index)
                metadata.transformations_applied.append("Conversión de índice a datetime")
            except Exception as e:
                metadata.warnings.append(f"No se pudo convertir índice a datetime: {e}")
        
        # 3. Ordenar por fecha
        cleaned = cleaned.sort_index()
        metadata.transformations_applied.append("Ordenamiento por fecha")
        
        # 4. Eliminar duplicados
        initial_rows = len(cleaned)
        cleaned = cleaned[~cleaned.index.duplicated(keep='first')]
        duplicates = initial_rows - len(cleaned)
        metadata.duplicates_removed = duplicates
        if duplicates > 0:
            metadata.transformations_applied.append(f"Eliminación de {duplicates} duplicados")
        
        # 5. Validar relaciones OHLC
        if self.validate_ohlc:
            invalid_mask = self._validate_ohlc(cleaned)
            invalid_count = invalid_mask.sum()
            if invalid_count > 0:
                metadata.invalid_ohlc_rows = invalid_count
                cleaned = cleaned[~invalid_mask]
                metadata.warnings.append(f"Se eliminaron {invalid_count} filas con relaciones OHLC inválidas")
                metadata.transformations_applied.append("Validación y eliminación de filas OHLC inválidas")
        
        # 6. Manejar valores nulos
        null_before = cleaned.isnull().sum().sum()
        
        if self.fill_method == 'drop':
            cleaned = cleaned.dropna()
            metadata.null_values_removed = null_before
            metadata.transformations_applied.append("Eliminación de filas con valores nulos")
        elif self.fill_method == 'forward':
            cleaned = cleaned.ffill()
            metadata.null_values_filled = null_before
            metadata.transformations_applied.append("Forward-fill de valores nulos")
        elif self.fill_method == 'backward':
            cleaned = cleaned.bfill()
            metadata.null_values_filled = null_before
            metadata.transformations_applied.append("Backward-fill de valores nulos")
        elif self.fill_method == 'interpolate':
            numeric_cols = cleaned.select_dtypes(include=[np.number]).columns
            cleaned[numeric_cols] = cleaned[numeric_cols].interpolate(method='time')
            metadata.null_values_filled = null_before
            metadata.transformations_applied.append("Interpolación de valores nulos")
        
        # 7. Asegurar tipos numéricos correctos
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_cols:
            if col in cleaned.columns:
                cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')
        
        # 8. Detectar y manejar outliers
        if self.remove_outliers:
            outliers = self._detect_outliers(cleaned)
            outlier_count = outliers.sum()
            if outlier_count > 0:
                metadata.outliers_detected = outlier_count
                cleaned = cleaned[~outliers]
                metadata.transformations_applied.append(f"Eliminación de {outlier_count} outliers")
        
        # 9. Añadir columnas auxiliares
        cleaned = self._add_price_features(cleaned)
        metadata.transformations_applied.append("Adición de columnas auxiliares (returns, log_returns, etc.)")
        
        # 10. Ajustar zona horaria (si es necesario)
        if cleaned.index.tz is not None:
            cleaned.index = cleaned.index.tz_localize(None)
            metadata.transformations_applied.append("Normalización de zona horaria")
        
        metadata.final_shape = cleaned.shape
        metadata.rows_removed = metadata.original_shape[0] - metadata.final_shape[0]
        
        logger.info(f"Limpieza completada. Filas: {metadata.original_shape[0]} -> {metadata.final_shape[0]}")
        
        return cleaned, metadata
    
    def clean_fundamental_data(self, 
                               data: Union[Dict, pd.DataFrame]) -> Tuple[Dict, CleaningMetadata]:
        """
        Limpia y normaliza datos fundamentales.
        
        Args:
            data: Diccionario o DataFrame con datos fundamentales
        
        Returns:
            Tuple con (datos limpios como dict, CleaningMetadata)
        """
        metadata = CleaningMetadata()
        
        logger.info("Limpiando datos fundamentales...")
        
        # Convertir a diccionario si es DataFrame
        if isinstance(data, pd.DataFrame):
            data = data.to_dict()
        
        cleaned = {}
        
        # Limpiar cada valor
        for key, value in data.items():
            # Normalizar nombre de clave
            clean_key = str(key).lower().strip() if self.normalize_column_names else str(key)
            
            # Manejar valores None/NaN
            if value is None or (isinstance(value, float) and np.isnan(value)):
                cleaned[clean_key] = None
                metadata.null_values_filled += 1
            elif isinstance(value, (int, float)):
                cleaned[clean_key] = float(value)
            elif isinstance(value, str):
                cleaned[clean_key] = value.strip()
            else:
                cleaned[clean_key] = value
        
        # Validar ratios básicos
        self._validate_fundamental_ratios(cleaned, metadata)
        
        metadata.transformations_applied.append("Normalización de datos fundamentales")
        metadata.transformations_applied.append("Validación de ratios básicos")
        
        logger.info("Limpieza de datos fundamentales completada")
        
        return cleaned, metadata
    
    def clean_financial_statement(self,
                                  data: pd.DataFrame,
                                  statement_type: str = "income") -> Tuple[pd.DataFrame, CleaningMetadata]:
        """
        Limpia y normaliza estados financieros.
        
        Args:
            data: DataFrame con estado financiero
            statement_type: Tipo de estado ("income", "balance", "cashflow")
        
        Returns:
            Tuple con (DataFrame limpio, CleaningMetadata)
        """
        metadata = CleaningMetadata()
        metadata.original_shape = data.shape
        
        logger.info(f"Limpiando {statement_type} statement...")
        
        cleaned = data.copy()
        
        # 1. Normalizar nombres de filas (métricas)
        if self.normalize_column_names:
            cleaned.index = [str(idx).strip() for idx in cleaned.index]
        
        # 2. Ordenar columnas cronológicamente (más reciente primero)
        if len(cleaned.columns) > 0:
            try:
                # Intentar ordenar por fecha si las columnas son fechas
                if isinstance(cleaned.columns[0], (pd.Timestamp, datetime)):
                    cleaned = cleaned.sort_index(axis=1, ascending=False)
                    metadata.transformations_applied.append("Ordenamiento cronológico de columnas")
            except:
                pass
        
        # 3. Manejar valores nulos
        null_before = cleaned.isnull().sum().sum()
        
        # Para estados financieros, generalmente no queremos imputar
        # pero podemos marcar con 0 o mantener NaN según el caso
        cleaned = cleaned.fillna(0)
        metadata.null_values_filled = null_before
        metadata.transformations_applied.append("Reemplazo de valores nulos con 0")
        
        # 4. Asegurar tipos numéricos
        numeric_cols = cleaned.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')
        
        # 5. Eliminar filas completamente vacías
        initial_rows = len(cleaned)
        cleaned = cleaned.loc[~(cleaned == 0).all(axis=1)]
        rows_removed = initial_rows - len(cleaned)
        if rows_removed > 0:
            metadata.rows_removed = rows_removed
            metadata.transformations_applied.append(f"Eliminación de {rows_removed} filas vacías")
        
        metadata.final_shape = cleaned.shape
        
        logger.info(f"Limpieza de {statement_type} statement completada")
        
        return cleaned, metadata
    
    def _validate_ohlc(self, data: pd.DataFrame) -> pd.Series:
        """
        Valida relaciones OHLC básicas.
        
        High >= max(Open, Close)
        Low <= min(Open, Close)
        """
        invalid_mask = pd.Series(False, index=data.index)
        
        required_cols = ['open', 'high', 'low', 'close']
        if not all(col in data.columns for col in required_cols):
            return invalid_mask
        
        # High debe ser >= Open y Close
        invalid_high = (data['high'] < data['open']) | (data['high'] < data['close'])
        
        # Low debe ser <= Open y Close
        invalid_low = (data['low'] > data['open']) | (data['low'] > data['close'])
        
        # Close debe estar entre Low y High
        invalid_close = (data['close'] < data['low']) | (data['close'] > data['high'])
        
        invalid_mask = invalid_high | invalid_low | invalid_close
        
        return invalid_mask
    
    def _detect_outliers(self, data: pd.DataFrame) -> pd.Series:
        """
        Detecta outliers usando el método de desviaciones estándar.
        """
        outlier_mask = pd.Series(False, index=data.index)
        
        # Solo aplicar a columnas de precios
        price_cols = ['open', 'high', 'low', 'close']
        for col in price_cols:
            if col in data.columns:
                z_scores = np.abs((data[col] - data[col].mean()) / data[col].std())
                outlier_mask |= z_scores > self.outlier_threshold
        
        return outlier_mask
    
    def _add_price_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Añade columnas auxiliares útiles para análisis.
        """
        result = data.copy()
        
        if 'close' not in result.columns:
            return result
        
        # Returns simples
        if 'close' in result.columns:
            result['returns'] = result['close'].pct_change()
            result['log_returns'] = np.log(result['close'] / result['close'].shift(1))
            result['price_change'] = result['close'].diff()
            result['pct_change'] = result['close'].pct_change() * 100
        
        # Volatilidad (rolling)
        if 'returns' in result.columns:
            result['volatility_20'] = result['returns'].rolling(window=20).std() * np.sqrt(252)
        
        return result
    
    def _validate_fundamental_ratios(self, data: Dict, metadata: CleaningMetadata):
        """
        Valida ratios fundamentales básicos.
        """
        # Validar que ratios positivos sean positivos
        positive_ratios = ['pe_ratio', 'price_to_book', 'price_to_sales', 'roe', 'roa']
        for ratio in positive_ratios:
            if ratio in data and data[ratio] is not None:
                if data[ratio] < 0:
                    metadata.warnings.append(f"{ratio} es negativo: {data[ratio]}")
        
        # Validar que porcentajes estén en rango razonable
        percentage_fields = ['dividend_yield', 'payout_ratio', 'profit_margin']
        for field in percentage_fields:
            if field in data and data[field] is not None:
                # Si está en formato decimal (0-1), convertir a porcentaje para validar
                value = data[field]
                if value < 1:  # Probablemente está en formato decimal
                    value = value * 100
                if value > 1000:  # Más del 1000% es sospechoso
                    metadata.warnings.append(f"{field} parece incorrecto: {value}%")


# Funciones de conveniencia
def clean_price_data(data: pd.DataFrame, 
                    symbol: Optional[str] = None,
                    **kwargs) -> Tuple[pd.DataFrame, CleaningMetadata]:
    """
    Función de conveniencia para limpiar datos de precios.
    
    Args:
        data: DataFrame con datos de precios
        symbol: Símbolo del activo (opcional)
        **kwargs: Argumentos adicionales para DataCleaner
    
    Returns:
        Tuple con (DataFrame limpio, CleaningMetadata)
    """
    cleaner = DataCleaner(**kwargs)
    return cleaner.clean_price_data(data, symbol=symbol)


def clean_fundamental_data(data: Union[Dict, pd.DataFrame],
                          **kwargs) -> Tuple[Dict, CleaningMetadata]:
    """
    Función de conveniencia para limpiar datos fundamentales.
    
    Args:
        data: Diccionario o DataFrame con datos fundamentales
        **kwargs: Argumentos adicionales para DataCleaner
    
    Returns:
        Tuple con (datos limpios, CleaningMetadata)
    """
    cleaner = DataCleaner(**kwargs)
    return cleaner.clean_fundamental_data(data)


def clean_financial_statement(data: pd.DataFrame,
                             statement_type: str = "income",
                             **kwargs) -> Tuple[pd.DataFrame, CleaningMetadata]:
    """
    Función de conveniencia para limpiar estados financieros.
    
    Args:
        data: DataFrame con estado financiero
        statement_type: Tipo de estado ("income", "balance", "cashflow")
        **kwargs: Argumentos adicionales para DataCleaner
    
    Returns:
        Tuple con (DataFrame limpio, CleaningMetadata)
    """
    cleaner = DataCleaner(**kwargs)
    return cleaner.clean_financial_statement(data, statement_type=statement_type)
