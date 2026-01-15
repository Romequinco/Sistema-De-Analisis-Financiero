"""
Análisis de Acción de Precio

Este módulo contiene herramientas para analizar la acción de precio
y patrones de mercado.

Indicadores implementados:
- Fractales: Identificación de máximos y mínimos locales
- Support/Resistance: niveles por swings
- Pivot Points: niveles clásicos
"""

import pandas as pd
import numpy as np


def calculate_fractals(df: pd.DataFrame,
                      period: int = 2,
                      output_prefix: str = 'Fractal') -> pd.DataFrame:
    """
    Identifica fractales (máximos y mínimos locales).
    
    Un fractal es un patrón de 5 barras donde:
    - Fractal Alcista: La barra del medio es el mínimo más bajo
    - Fractal Bajista: La barra del medio es el máximo más alto
    
    Los fractales ayudan a identificar niveles de soporte y resistencia
    potenciales y puntos de reversión.
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low'.
        period: Número de barras a cada lado para comparar (default: 2).
            Con period=2, se compara con 2 barras antes y 2 después (total 5 barras).
        output_prefix: Prefijo para las columnas de salida (default: 'Fractal').
            Se crearán:
            - {prefix}_Up: Fractales alcistas (mínimos locales)
            - {prefix}_Down: Fractales bajistas (máximos locales)
    
    Returns:
        DataFrame con nuevas columnas para fractales alcistas y bajistas.
    
    Ejemplo:
        >>> df = calculate_fractals(df, period=2)
        >>> df['Fractal_Up']  # True donde hay fractal alcista
        >>> df['Fractal_Down']  # True donde hay fractal bajista
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    high = df['high'].values
    low = df['low'].values
    
    # Inicializar arrays
    fractal_up = np.zeros(len(df), dtype=bool)
    fractal_down = np.zeros(len(df), dtype=bool)
    
    # Identificar fractales
    for i in range(period, len(df) - period):
        # Fractal alcista: low[i] es el mínimo más bajo en el rango
        is_fractal_up = True
        for j in range(i - period, i + period + 1):
            if j != i and low[j] <= low[i]:
                is_fractal_up = False
                break
        
        if is_fractal_up:
            fractal_up[i] = True
        
        # Fractal bajista: high[i] es el máximo más alto en el rango
        is_fractal_down = True
        for j in range(i - period, i + period + 1):
            if j != i and high[j] >= high[i]:
                is_fractal_down = False
                break
        
        if is_fractal_down:
            fractal_down[i] = True
    
    # Añadir al DataFrame
    df[f'{output_prefix}_Up'] = fractal_up
    df[f'{output_prefix}_Down'] = fractal_down
    
    return df


def calculate_support_resistance(df: pd.DataFrame,
                                 lookback: int = 2,
                                 output_prefix: str = 'SR') -> pd.DataFrame:
    """
    Calcula soporte y resistencia basados en swings.
    """
    df = df.copy()

    required_cols = ['high', 'low']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")

    window = 2 * lookback + 1
    swing_high = df['high'] == df['high'].rolling(window=window, center=True).max()
    swing_low = df['low'] == df['low'].rolling(window=window, center=True).min()

    resistance = df['high'].where(swing_high).ffill()
    support = df['low'].where(swing_low).ffill()

    df[f'{output_prefix}_Swing_High'] = swing_high
    df[f'{output_prefix}_Swing_Low'] = swing_low
    df[f'{output_prefix}_Resistance'] = resistance
    df[f'{output_prefix}_Support'] = support

    return df


def calculate_pivot_points(df: pd.DataFrame,
                           output_prefix: str = 'Pivot') -> pd.DataFrame:
    """
    Calcula Pivot Points clasicos (PP, R1/R2, S1/S2).
    """
    df = df.copy()

    required_cols = ['high', 'low', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")

    prev_high = df['high'].shift(1)
    prev_low = df['low'].shift(1)
    prev_close = df['close'].shift(1)

    pp = (prev_high + prev_low + prev_close) / 3
    r1 = 2 * pp - prev_low
    s1 = 2 * pp - prev_high
    r2 = pp + (prev_high - prev_low)
    s2 = pp - (prev_high - prev_low)

    df[f'{output_prefix}_PP'] = pp
    df[f'{output_prefix}_R1'] = r1
    df[f'{output_prefix}_S1'] = s1
    df[f'{output_prefix}_R2'] = r2
    df[f'{output_prefix}_S2'] = s2

    return df
