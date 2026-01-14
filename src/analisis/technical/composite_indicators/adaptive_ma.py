"""
Adaptive Moving Averages

Medias móviles adaptativas que ajustan su velocidad según las condiciones
del mercado (volatilidad, tendencia, etc.).
"""

import pandas as pd
import numpy as np
from typing import Optional
from ..indicators.volatility import calculate_atr
from ..indicators.trend import calculate_ema


def calculate_adaptive_ma(df: pd.DataFrame,
                          period: int = 14,
                          fast_period: int = 2,
                          slow_period: int = 30,
                          output_column: str = 'Adaptive_MA') -> pd.DataFrame:
    """
    Calcula una Media Móvil Adaptativa basada en volatilidad.
    
    Esta implementación ajusta la velocidad de la media móvil según
    la volatilidad del mercado medida por el ATR. Cuando la volatilidad
    es alta, la media se vuelve más rápida (más sensible). Cuando la
    volatilidad es baja, la media se vuelve más lenta (más suave).
    
    El factor de adaptación se calcula como:
    - Factor = (ATR actual / ATR promedio) normalizado
    - Período efectivo = Período base ajustado por el factor
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close'.
        period: Período base para el cálculo (default: 14).
        fast_period: Período mínimo (más rápido) (default: 2).
        slow_period: Período máximo (más lento) (default: 30).
        output_column: Nombre de la columna de salida (default: 'Adaptive_MA').
    
    Returns:
        DataFrame con una nueva columna 'Adaptive_MA'.
    
    Ejemplo:
        >>> df = calculate_adaptive_ma(df)
        >>> df['Adaptive_MA']  # Media móvil adaptativa
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    # Calcular ATR
    df = calculate_atr(df, period=period, output_column='ATR_temp')
    
    # Calcular ATR promedio
    atr_avg = df['ATR_temp'].rolling(window=period, min_periods=1).mean()
    
    # Calcular factor de adaptación
    # Normalizar ATR relativo al promedio
    atr_ratio = df['ATR_temp'] / atr_avg
    atr_ratio = atr_ratio.replace([np.inf, -np.inf], 1.0).fillna(1.0)
    
    # Limitar el ratio entre 0.5 y 2.0 para evitar extremos
    atr_ratio = atr_ratio.clip(lower=0.5, upper=2.0)
    
    # Calcular período efectivo adaptativo
    # Mayor volatilidad = período más corto (más rápido)
    # Menor volatilidad = período más largo (más lento)
    effective_period = slow_period / atr_ratio
    effective_period = effective_period.clip(lower=fast_period, upper=slow_period)
    
    # Calcular EMA adaptativa usando período efectivo variable
    # Usamos un promedio ponderado de múltiples EMAs
    adaptive_ma = pd.Series(index=df.index, dtype=float)
    
    for i in range(len(df)):
        if i == 0:
            adaptive_ma.iloc[i] = df['close'].iloc[i]
        else:
            # Calcular EMA con período efectivo actual
            eff_period = effective_period.iloc[i]
            alpha = 2.0 / (eff_period + 1.0)
            adaptive_ma.iloc[i] = alpha * df['close'].iloc[i] + (1 - alpha) * adaptive_ma.iloc[i-1]
    
    # Añadir al DataFrame
    df[output_column] = adaptive_ma
    
    # Eliminar columna temporal
    df = df.drop(columns=['ATR_temp'])
    
    return df
