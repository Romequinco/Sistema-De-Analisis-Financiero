"""
Análisis de Acción de Precio

Este módulo contiene herramientas para analizar la acción de precio
y patrones de mercado.

Indicadores implementados:
- Fractales: Identificación de máximos y mínimos locales
- Wyckoff: Conceptos básicos (análisis conceptual, no automático)
"""

import pandas as pd
import numpy as np
from typing import Optional


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


def identify_wyckoff_phases(df: pd.DataFrame,
                            output_column: str = 'Wyckoff_Phase') -> pd.DataFrame:
    """
    Identifica fases básicas del método Wyckoff (conceptual).
    
    NOTA: Esta es una implementación simplificada y conceptual.
    El análisis Wyckoff completo requiere interpretación manual
    y análisis de múltiples factores (precio, volumen, tiempo).
    
    Las fases identificadas son:
    - 'Accumulation': Acumulación (fase inicial de compra institucional)
    - 'Markup': Subida (tendencia alcista)
    - 'Distribution': Distribución (fase inicial de venta institucional)
    - 'Markdown': Bajada (tendencia bajista)
    - 'Unknown': No determinado
    
    Esta función usa heurísticas simples basadas en:
    - Tendencia de precio
    - Volumen relativo
    - Volatilidad
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close', 'volume'.
        output_column: Nombre de la columna de salida (default: 'Wyckoff_Phase').
    
    Returns:
        DataFrame con una nueva columna 'Wyckoff_Phase' con valores categóricos.
    
    Ejemplo:
        >>> df = identify_wyckoff_phases(df)
        >>> df['Wyckoff_Phase']  # Fase identificada
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    # Calcular métricas necesarias
    df['price_change'] = df['close'].pct_change()
    df['volume_avg'] = df['volume'].rolling(window=20, min_periods=1).mean()
    df['volume_ratio'] = df['volume'] / df['volume_avg']
    
    # Calcular volatilidad (ATR simplificado)
    high_low = df['high'] - df['low']
    df['volatility'] = high_low.rolling(window=14, min_periods=1).mean()
    df['volatility_avg'] = df['volatility'].rolling(window=20, min_periods=1).mean()
    df['volatility_ratio'] = df['volatility'] / df['volatility_avg']
    
    # Identificar fases usando heurísticas simples
    phases = []
    
    for i in range(len(df)):
        if i < 20:  # No hay suficientes datos
            phases.append('Unknown')
            continue
        
        price_change = df['price_change'].iloc[i]
        volume_ratio = df['volume_ratio'].iloc[i]
        volatility_ratio = df['volatility_ratio'].iloc[i]
        
        # Heurísticas simplificadas
        if price_change > 0.01 and volume_ratio > 1.2 and volatility_ratio < 1.0:
            phases.append('Markup')  # Subida con volumen alto y volatilidad baja
        elif price_change < -0.01 and volume_ratio > 1.2 and volatility_ratio < 1.0:
            phases.append('Markdown')  # Bajada con volumen alto y volatilidad baja
        elif abs(price_change) < 0.005 and volume_ratio > 1.1 and volatility_ratio < 0.9:
            phases.append('Accumulation')  # Lateral con volumen alto (acumulación)
        elif abs(price_change) < 0.005 and volume_ratio > 1.1 and volatility_ratio < 0.9:
            phases.append('Distribution')  # Lateral con volumen alto (distribución)
        else:
            phases.append('Unknown')
    
    # Añadir al DataFrame
    df[output_column] = phases
    
    # Limpiar columnas temporales
    df = df.drop(columns=['price_change', 'volume_avg', 'volume_ratio',
                          'volatility', 'volatility_avg', 'volatility_ratio'])
    
    return df
