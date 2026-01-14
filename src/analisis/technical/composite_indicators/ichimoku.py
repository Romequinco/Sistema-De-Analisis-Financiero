"""
Ichimoku Cloud (Nube de Ichimoku)

Sistema completo de análisis técnico japonés que proporciona múltiples
líneas y una nube (Kumo) para identificar tendencias, soportes/resistencias
y momentum.
"""

import pandas as pd
import numpy as np
from typing import Optional
from ..indicators.trend import calculate_sma


def calculate_ichimoku(df: pd.DataFrame,
                       tenkan_period: int = 9,
                       kijun_period: int = 26,
                       senkou_b_period: int = 52,
                       chikou_offset: int = 26,
                       output_prefix: str = 'Ichimoku') -> pd.DataFrame:
    """
    Calcula el sistema Ichimoku completo.
    
    El sistema Ichimoku consta de 5 componentes:
    
    1. Tenkan-sen (Línea de Conversión): (High más alto + Low más bajo) / 2 (9 períodos)
    2. Kijun-sen (Línea Base): (High más alto + Low más bajo) / 2 (26 períodos)
    3. Senkou Span A (Línea Líder A): (Tenkan + Kijun) / 2, desplazada 26 períodos adelante
    4. Senkou Span B (Línea Líder B): (High más alto + Low más bajo) / 2 (52 períodos), desplazada 26 períodos adelante
    5. Chikou Span (Línea Retrasada): Precio de cierre desplazado 26 períodos atrás
    
    La nube (Kumo) es el área entre Senkou Span A y Senkou Span B.
    
    Interpretación:
    - Precio por encima de la nube: Tendencia alcista
    - Precio por debajo de la nube: Tendencia bajista
    - Precio dentro de la nube: Tendencia neutral/indecisa
    - Nube verde (Span A > Span B): Momentum alcista
    - Nube roja (Span A < Span B): Momentum bajista
    - Tenkan cruza Kijun: Señal de cambio de tendencia
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close'.
        tenkan_period: Período para Tenkan-sen (default: 9).
        kijun_period: Período para Kijun-sen (default: 26).
        senkou_b_period: Período para Senkou Span B (default: 52).
        chikou_offset: Desplazamiento para Chikou Span (default: 26).
        output_prefix: Prefijo para las columnas de salida (default: 'Ichimoku').
            Se crearán:
            - {prefix}_Tenkan: Tenkan-sen
            - {prefix}_Kijun: Kijun-sen
            - {prefix}_Senkou_A: Senkou Span A
            - {prefix}_Senkou_B: Senkou Span B
            - {prefix}_Chikou: Chikou Span
            - {prefix}_Cloud_Top: Parte superior de la nube
            - {prefix}_Cloud_Bottom: Parte inferior de la nube
    
    Returns:
        DataFrame con nuevas columnas para todos los componentes de Ichimoku.
    
    Ejemplo:
        >>> df = calculate_ichimoku(df)
        >>> df['Ichimoku_Tenkan']  # Línea de conversión
        >>> df['Ichimoku_Senkou_A']  # Línea líder A
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values
    
    # Calcular Tenkan-sen: (High más alto + Low más bajo) / 2
    tenkan_high = df['high'].rolling(window=tenkan_period, min_periods=1).max()
    tenkan_low = df['low'].rolling(window=tenkan_period, min_periods=1).min()
    tenkan = (tenkan_high + tenkan_low) / 2
    
    # Calcular Kijun-sen: (High más alto + Low más bajo) / 2
    kijun_high = df['high'].rolling(window=kijun_period, min_periods=1).max()
    kijun_low = df['low'].rolling(window=kijun_period, min_periods=1).min()
    kijun = (kijun_high + kijun_low) / 2
    
    # Calcular Senkou Span A: (Tenkan + Kijun) / 2, desplazada hacia adelante
    senkou_a = (tenkan + kijun) / 2
    senkou_a_shifted = senkou_a.shift(chikou_offset)
    
    # Calcular Senkou Span B: (High más alto + Low más bajo) / 2, desplazada hacia adelante
    senkou_b_high = df['high'].rolling(window=senkou_b_period, min_periods=1).max()
    senkou_b_low = df['low'].rolling(window=senkou_b_period, min_periods=1).min()
    senkou_b = (senkou_b_high + senkou_b_low) / 2
    senkou_b_shifted = senkou_b.shift(chikou_offset)
    
    # Calcular Chikou Span: Close desplazado hacia atrás
    chikou = df['close'].shift(-chikou_offset)
    
    # Calcular partes superior e inferior de la nube
    cloud_top = pd.concat([senkou_a_shifted, senkou_b_shifted], axis=1).max(axis=1)
    cloud_bottom = pd.concat([senkou_a_shifted, senkou_b_shifted], axis=1).min(axis=1)
    
    # Añadir al DataFrame
    df[f'{output_prefix}_Tenkan'] = tenkan
    df[f'{output_prefix}_Kijun'] = kijun
    df[f'{output_prefix}_Senkou_A'] = senkou_a_shifted
    df[f'{output_prefix}_Senkou_B'] = senkou_b_shifted
    df[f'{output_prefix}_Chikou'] = chikou
    df[f'{output_prefix}_Cloud_Top'] = cloud_top
    df[f'{output_prefix}_Cloud_Bottom'] = cloud_bottom
    
    return df
