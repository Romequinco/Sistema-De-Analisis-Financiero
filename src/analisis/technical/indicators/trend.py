"""
Indicadores de Tendencia

Este módulo contiene indicadores técnicos que ayudan a identificar
la dirección y fuerza de las tendencias en el precio.

Indicadores implementados:
- SMA: Simple Moving Average
- EMA: Exponential Moving Average
- HMA: Hull Moving Average
"""

import pandas as pd
import numpy as np
from typing import Iterable, Optional, Tuple

DEFAULT_MA_PERIODS: Tuple[int, int, int] = (8, 18, 40)


def calculate_sma(df: pd.DataFrame, 
                   column: str = 'close',
                   period: int = 20,
                   output_column: Optional[str] = None) -> pd.DataFrame:
    """
    Calcula la Media Móvil Simple (SMA).
    
    La SMA es el promedio aritmético de los precios de cierre durante
    un período determinado. Es uno de los indicadores de tendencia más
    básicos y ampliamente utilizados.
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'close' o la especificada.
        column: Nombre de la columna de precio a usar (default: 'close').
        period: Período para el cálculo (default: 20).
        output_column: Nombre de la columna de salida. Si es None, usa 'SMA_{period}'.
    
    Returns:
        DataFrame con una nueva columna 'SMA_{period}' o el nombre especificado.
    
    Ejemplo:
        >>> df = calculate_sma(df, period=18)
        >>> df['SMA_18']  # Acceder a la SMA de 18 períodos
    """
    df = df.copy()
    
    # Normalizar nombre de columna
    column = column.lower()
    if column not in df.columns:
        raise ValueError(f"Columna '{column}' no encontrada en el DataFrame")
    
    # Nombre de columna de salida
    if output_column is None:
        output_column = f'SMA_{period}'
    
    # Calcular SMA
    df[output_column] = df[column].rolling(window=period, min_periods=1).mean()
    
    return df


def calculate_ema(df: pd.DataFrame,
                  column: str = 'close',
                  period: int = 20,
                  output_column: Optional[str] = None) -> pd.DataFrame:
    """
    Calcula la Media Móvil Exponencial (EMA).
    
    La EMA da más peso a los precios recientes, lo que la hace más
    sensible a cambios recientes en el precio comparada con la SMA.
    Esto la hace útil para identificar cambios de tendencia más rápido.
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'close' o la especificada.
        column: Nombre de la columna de precio a usar (default: 'close').
        period: Período para el cálculo (default: 20).
        output_column: Nombre de la columna de salida. Si es None, usa 'EMA_{period}'.
    
    Returns:
        DataFrame con una nueva columna 'EMA_{period}' o el nombre especificado.
    
    Ejemplo:
        >>> df = calculate_ema(df, period=18)
        >>> df['EMA_18']  # Acceder a la EMA de 18 períodos
    """
    df = df.copy()
    
    # Normalizar nombre de columna
    column = column.lower()
    if column not in df.columns:
        raise ValueError(f"Columna '{column}' no encontrada en el DataFrame")
    
    # Nombre de columna de salida
    if output_column is None:
        output_column = f'EMA_{period}'
    
    # Calcular EMA usando pandas (método exponencial)
    df[output_column] = df[column].ewm(span=period, adjust=False, min_periods=1).mean()
    
    return df


def _weighted_moving_average(series: pd.Series, period: int) -> pd.Series:
    if period < 1:
        raise ValueError("El periodo debe ser >= 1")
    weights = np.arange(1, period + 1, dtype=float)
    return series.rolling(window=period, min_periods=period).apply(
        lambda x: np.dot(x, weights) / weights.sum(),
        raw=True
    )


def calculate_hma(df: pd.DataFrame,
                  column: str = 'close',
                  period: int = 20,
                  output_column: Optional[str] = None) -> pd.DataFrame:
    """
    Calcula la Hull Moving Average (HMA).

    La HMA combina rapidez y suavizado reduciendo el lag respecto a SMA/EMA.
    Default period=20 como compromiso entre velocidad y ruido.
    """
    df = df.copy()

    column = column.lower()
    if column not in df.columns:
        raise ValueError(f"Columna '{column}' no encontrada en el DataFrame")
    if period < 2:
        raise ValueError("El periodo debe ser >= 2 para HMA")

    if output_column is None:
        output_column = f'HMA_{period}'

    half_period = max(1, period // 2)
    sqrt_period = max(1, int(np.sqrt(period)))

    wma_half = _weighted_moving_average(df[column], half_period)
    wma_full = _weighted_moving_average(df[column], period)
    hma_raw = 2 * wma_half - wma_full
    df[output_column] = _weighted_moving_average(hma_raw, sqrt_period)

    return df


def calculate_sma_series(df: pd.DataFrame,
                         column: str = 'close',
                         periods: Iterable[int] = DEFAULT_MA_PERIODS,
                         output_prefix: str = 'SMA') -> pd.DataFrame:
    """
    Calcula múltiples SMAs para una lista de períodos.

    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'close' o la especificada.
        column: Nombre de la columna de precio a usar (default: 'close').
        periods: Períodos a calcular (default: 8, 18, 40).
        output_prefix: Prefijo para columnas de salida (default: 'SMA').

    Returns:
        DataFrame con nuevas columnas SMA por período.
    """
    df = df.copy()

    column = column.lower()
    if column not in df.columns:
        raise ValueError(f"Columna '{column}' no encontrada en el DataFrame")

    for period in periods:
        output_column = f'{output_prefix}_{period}'
        df[output_column] = df[column].rolling(window=period, min_periods=1).mean()

    return df


def calculate_ema_series(df: pd.DataFrame,
                         column: str = 'close',
                         periods: Iterable[int] = DEFAULT_MA_PERIODS,
                         output_prefix: str = 'EMA') -> pd.DataFrame:
    """
    Calcula múltiples EMAs para una lista de períodos.

    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'close' o la especificada.
        column: Nombre de la columna de precio a usar (default: 'close').
        periods: Períodos a calcular (default: 8, 18, 40).
        output_prefix: Prefijo para columnas de salida (default: 'EMA').

    Returns:
        DataFrame con nuevas columnas EMA por período.
    """
    df = df.copy()

    column = column.lower()
    if column not in df.columns:
        raise ValueError(f"Columna '{column}' no encontrada en el DataFrame")

    for period in periods:
        output_column = f'{output_prefix}_{period}'
        df[output_column] = df[column].ewm(span=period, adjust=False, min_periods=1).mean()

    return df


