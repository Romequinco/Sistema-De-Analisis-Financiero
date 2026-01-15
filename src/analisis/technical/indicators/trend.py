"""
Indicadores de Tendencia

Este módulo contiene indicadores técnicos que ayudan a identificar
la dirección y fuerza de las tendencias en el precio.

Indicadores implementados:
- SMA: Simple Moving Average
- EMA: Exponential Moving Average
- Parabolic SAR: Stop and Reverse parabólico
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


def calculate_parabolic_sar(df: pd.DataFrame,
                            af_start: float = 0.02,
                            af_increment: float = 0.02,
                            af_max: float = 0.2,
                            output_column: str = 'Parabolic_SAR') -> pd.DataFrame:
    """
    Calcula el Parabolic SAR (Stop and Reverse).
    
    El Parabolic SAR es un indicador de tendencia que muestra puntos
    potenciales de reversión de precio. Se representa como puntos
    por encima o debajo del precio, indicando la dirección de la tendencia.
    
    Cuando el SAR está por debajo del precio, la tendencia es alcista.
    Cuando el SAR está por encima del precio, la tendencia es bajista.
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close'.
        af_start: Factor de aceleración inicial (default: 0.02).
        af_increment: Incremento del factor de aceleración (default: 0.02).
        af_max: Factor de aceleración máximo (default: 0.2).
        output_column: Nombre de la columna de salida (default: 'Parabolic_SAR').
    
    Returns:
        DataFrame con una nueva columna 'Parabolic_SAR'.
    
    Ejemplo:
        >>> df = calculate_parabolic_sar(df)
        >>> df['Parabolic_SAR']  # Acceder al Parabolic SAR
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    # Inicializar arrays
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values
    sar = np.zeros(len(df))
    trend = np.zeros(len(df), dtype=int)  # 1 = alcista, -1 = bajista
    ep = np.zeros(len(df))  # Extreme Point
    af = np.zeros(len(df))  # Acceleration Factor
    
    # Inicializar primer valor
    sar[0] = low[0]
    trend[0] = 1  # Empezar con tendencia alcista
    ep[0] = high[0]
    af[0] = af_start
    
    # Calcular SAR para cada período
    for i in range(1, len(df)):
        # SAR anterior
        sar_prev = sar[i-1]
        trend_prev = trend[i-1]
        ep_prev = ep[i-1]
        af_prev = af[i-1]
        
        if trend_prev == 1:  # Tendencia alcista
            # Calcular nuevo SAR
            sar[i] = sar_prev + af_prev * (ep_prev - sar_prev)
            
            # El SAR no puede estar por encima del low anterior o actual
            sar[i] = min(sar[i], low[i-1], low[i])
            
            # Actualizar EP si hay nuevo máximo
            if high[i] > ep_prev:
                ep[i] = high[i]
                af[i] = min(af_prev + af_increment, af_max)
            else:
                ep[i] = ep_prev
                af[i] = af_prev
            
            # Verificar cambio de tendencia
            if low[i] < sar[i]:
                trend[i] = -1  # Cambio a bajista
                sar[i] = ep_prev
                ep[i] = low[i]
                af[i] = af_start
            else:
                trend[i] = 1
        
        else:  # Tendencia bajista
            # Calcular nuevo SAR
            sar[i] = sar_prev + af_prev * (ep_prev - sar_prev)
            
            # El SAR no puede estar por debajo del high anterior o actual
            sar[i] = max(sar[i], high[i-1], high[i])
            
            # Actualizar EP si hay nuevo mínimo
            if low[i] < ep_prev:
                ep[i] = low[i]
                af[i] = min(af_prev + af_increment, af_max)
            else:
                ep[i] = ep_prev
                af[i] = af_prev
            
            # Verificar cambio de tendencia
            if high[i] > sar[i]:
                trend[i] = 1  # Cambio a alcista
                sar[i] = ep_prev
                ep[i] = high[i]
                af[i] = af_start
            else:
                trend[i] = -1
    
    # Añadir al DataFrame
    df[output_column] = sar
    
    return df
