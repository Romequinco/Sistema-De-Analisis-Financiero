"""
MACD (Moving Average Convergence Divergence)

Indicador compuesto que combina múltiples medias móviles exponenciales
para identificar cambios en momentum, tendencia y posibles reversiones.
"""

import pandas as pd
import numpy as np
from typing import Optional
from ..indicators.trend import calculate_ema


def calculate_macd(df: pd.DataFrame,
                   fast_period: int = 12,
                   slow_period: int = 26,
                   signal_period: int = 9,
                   output_prefix: str = 'MACD') -> pd.DataFrame:
    """
    Calcula el MACD (Moving Average Convergence Divergence).
    
    El MACD es un indicador de momentum que muestra la relación entre
    dos medias móviles exponenciales del precio. Consiste en:
    
    - MACD Line: Diferencia entre EMA rápida (12) y EMA lenta (26)
    - Signal Line: EMA del MACD Line (9 períodos)
    - Histogram: Diferencia entre MACD Line y Signal Line
    
    Interpretación:
    - Cruce alcista: MACD cruza por encima de Signal (señal de compra)
    - Cruce bajista: MACD cruza por debajo de Signal (señal de venta)
    - Divergencia: MACD y precio se mueven en direcciones opuestas
    - Histogram positivo: Momentum alcista
    - Histogram negativo: Momentum bajista
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'close'.
        fast_period: Período de la EMA rápida (default: 12).
        slow_period: Período de la EMA lenta (default: 26).
        signal_period: Período de la Signal Line (default: 9).
        output_prefix: Prefijo para las columnas de salida (default: 'MACD').
            Se crearán:
            - {prefix}_Line: Línea MACD
            - {prefix}_Signal: Línea de señal
            - {prefix}_Histogram: Histograma (MACD - Signal)
    
    Returns:
        DataFrame con nuevas columnas para MACD, Signal e Histogram.
    
    Ejemplo:
        >>> df = calculate_macd(df)
        >>> df['MACD_Line']  # Línea MACD
        >>> df['MACD_Signal']  # Línea de señal
        >>> df['MACD_Histogram']  # Histograma
    """
    df = df.copy()
    
    # Validar columna de cierre
    if 'close' not in df.columns:
        raise ValueError("Columna 'close' no encontrada en el DataFrame")
    
    # Calcular EMAs rápida y lenta
    df = calculate_ema(df, column='close', period=fast_period, 
                       output_column=f'EMA_{fast_period}')
    df = calculate_ema(df, column='close', period=slow_period,
                       output_column=f'EMA_{slow_period}')
    
    # Calcular MACD Line (diferencia entre EMAs)
    macd_line = df[f'EMA_{fast_period}'] - df[f'EMA_{slow_period}']
    
    # Calcular Signal Line (EMA del MACD Line)
    # Usar método directo para Signal Line
    signal_line = macd_line.ewm(span=signal_period, adjust=False, min_periods=1).mean()
    
    # Calcular Histogram (diferencia entre MACD y Signal)
    histogram = macd_line - signal_line
    
    # Añadir al DataFrame
    df[f'{output_prefix}_Line'] = macd_line
    df[f'{output_prefix}_Signal'] = signal_line
    df[f'{output_prefix}_Histogram'] = histogram
    
    # Eliminar columnas temporales
    df = df.drop(columns=[f'EMA_{fast_period}', f'EMA_{slow_period}'])
    
    return df
