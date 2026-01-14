"""
SuperTrend

Indicador de tendencia que se adapta a la volatilidad del mercado usando ATR.
Proporciona señales claras de tendencia y puntos de reversión.
"""

import pandas as pd
import numpy as np
from typing import Optional
from ..indicators.volatility import calculate_atr


def calculate_supertrend(df: pd.DataFrame,
                        period: int = 10,
                        multiplier: float = 3.0,
                        output_column: str = 'SuperTrend') -> pd.DataFrame:
    """
    Calcula el SuperTrend.
    
    El SuperTrend es un indicador de tendencia que se adapta a la volatilidad
    usando el ATR. Proporciona una línea que cambia de color según la tendencia:
    - Verde (por debajo del precio): Tendencia alcista
    - Rojo (por encima del precio): Tendencia bajista
    
    El SuperTrend se calcula como:
    1. Calcular ATR
    2. Calcular bandas superior e inferior usando ATR × multiplicador
    3. Determinar la tendencia basándose en la posición del precio
    4. Ajustar el SuperTrend según la tendencia
    
    Interpretación:
    - SuperTrend por debajo del precio: Tendencia alcista (señal de compra)
    - SuperTrend por encima del precio: Tendencia bajista (señal de venta)
    - Cambio de color: Posible cambio de tendencia
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close'.
        period: Período para el cálculo del ATR (default: 10).
        multiplier: Multiplicador del ATR (default: 3.0).
        output_column: Nombre base para las columnas de salida (default: 'SuperTrend').
            Se crearán:
            - {output_column}: Valor del SuperTrend
            - {output_column}_Trend: Tendencia (1 = alcista, -1 = bajista)
    
    Returns:
        DataFrame con nuevas columnas para SuperTrend y tendencia.
    
    Ejemplo:
        >>> df = calculate_supertrend(df, period=10, multiplier=3.0)
        >>> df['SuperTrend']  # Valor del SuperTrend
        >>> df['SuperTrend_Trend']  # Dirección de la tendencia
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    # Calcular ATR
    df = calculate_atr(df, period=period, output_column='ATR_temp')
    
    # Calcular bandas básicas
    hl_avg = (df['high'] + df['low']) / 2
    upper_band = hl_avg + (multiplier * df['ATR_temp'])
    lower_band = hl_avg - (multiplier * df['ATR_temp'])
    
    # Inicializar arrays
    supertrend = np.zeros(len(df))
    trend = np.zeros(len(df), dtype=int)
    
    # Calcular SuperTrend
    for i in range(len(df)):
        if i == 0:
            supertrend[i] = upper_band.iloc[i]
            trend[i] = -1  # Empezar con tendencia bajista
        else:
            # Ajustar bandas según la tendencia anterior
            if df['close'].iloc[i] <= supertrend[i-1]:
                # Tendencia bajista
                supertrend[i] = upper_band.iloc[i]
                trend[i] = -1
            else:
                # Tendencia alcista
                supertrend[i] = lower_band.iloc[i]
                trend[i] = 1
            
            # Asegurar que el SuperTrend no cruce el precio
            if trend[i] == 1 and supertrend[i] > df['close'].iloc[i]:
                supertrend[i] = df['close'].iloc[i]
            elif trend[i] == -1 and supertrend[i] < df['close'].iloc[i]:
                supertrend[i] = df['close'].iloc[i]
            
            # Ajustar si la banda cruza el precio
            if trend[i] == 1 and df['close'].iloc[i] < lower_band.iloc[i]:
                supertrend[i] = upper_band.iloc[i]
                trend[i] = -1
            elif trend[i] == -1 and df['close'].iloc[i] > upper_band.iloc[i]:
                supertrend[i] = lower_band.iloc[i]
                trend[i] = 1
    
    # Añadir al DataFrame
    df[output_column] = supertrend
    df[f'{output_column}_Trend'] = trend
    
    # Eliminar columna temporal
    df = df.drop(columns=['ATR_temp'])
    
    return df
