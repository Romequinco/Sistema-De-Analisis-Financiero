"""
Indicadores de Volatilidad

Este módulo contiene indicadores técnicos que miden la volatilidad
y la variabilidad de los precios.

Indicadores implementados:
- ATR: Average True Range
- Bollinger Bands: Bandas de Bollinger
"""

import pandas as pd
import numpy as np
from typing import Optional


def calculate_atr(df: pd.DataFrame,
                  period: int = 14,
                  output_column: Optional[str] = None) -> pd.DataFrame:
    """
    Calcula el Average True Range (ATR).
    
    El ATR mide la volatilidad del mercado calculando el promedio
    del True Range durante un período determinado. No indica dirección,
    solo volatilidad.
    
    Interpretación:
    - ATR alto: Alta volatilidad (mercado volátil)
    - ATR bajo: Baja volatilidad (mercado tranquilo)
    
    El True Range es el mayor de:
    1. High - Low
    2. |High - Close anterior|
    3. |Low - Close anterior|
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close'.
        period: Período para el cálculo (default: 14).
        output_column: Nombre de la columna de salida. Si es None, usa 'ATR_{period}'.
    
    Returns:
        DataFrame con una nueva columna 'ATR_{period}' o el nombre especificado.
    
    Ejemplo:
        >>> df = calculate_atr(df, period=14)
        >>> df['ATR_14']  # Acceder al ATR de 14 períodos
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    # Nombre de columna de salida
    if output_column is None:
        output_column = f'ATR_{period}'
    
    # Calcular True Range
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values
    
    tr_list = []
    for i in range(len(df)):
        if i == 0:
            tr = high[i] - low[i]
        else:
            tr1 = high[i] - low[i]
            tr2 = abs(high[i] - close[i-1])
            tr3 = abs(low[i] - close[i-1])
            tr = max(tr1, tr2, tr3)
        tr_list.append(tr)
    
    # Calcular ATR usando método Wilder (promedio exponencial)
    tr_series = pd.Series(tr_list)
    
    # Primera iteración: promedio simple
    atr = tr_series.rolling(window=period, min_periods=period).mean()
    
    # Iteraciones siguientes: promedio exponencial (método Wilder)
    for i in range(period, len(df)):
        if i == period:
            continue
        atr.iloc[i] = (atr.iloc[i-1] * (period - 1) + tr_list[i]) / period
    
    # Añadir al DataFrame
    df[output_column] = atr
    
    return df


def calculate_bollinger_bands(df: pd.DataFrame,
                              column: str = 'close',
                              period: int = 20,
                              std_dev: float = 2.0,
                              output_prefix: Optional[str] = None) -> pd.DataFrame:
    """
    Calcula las Bandas de Bollinger.
    
    Las Bandas de Bollinger consisten en:
    - Banda Media: SMA del precio
    - Banda Superior: SMA + (desviación estándar × multiplicador)
    - Banda Inferior: SMA - (desviación estándar × multiplicador)
    
    Interpretación:
    - Precio cerca de banda superior: Posible sobrecompra
    - Precio cerca de banda inferior: Posible sobreventa
    - Bandas se expanden: Aumento de volatilidad
    - Bandas se contraen: Disminución de volatilidad
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'close' o la especificada.
        column: Nombre de la columna de precio a usar (default: 'close').
        period: Período para el cálculo de la SMA (default: 20).
        std_dev: Número de desviaciones estándar (default: 2.0).
        output_prefix: Prefijo para las columnas de salida. Si es None, usa 'BB_{period}'.
            Se crearán:
            - {prefix}_Upper: Banda superior
            - {prefix}_Middle: Banda media (SMA)
            - {prefix}_Lower: Banda inferior
            - {prefix}_Width: Ancho de las bandas (Upper - Lower)
            - {prefix}_PercentB: Porcentaje B (posición del precio relativo a las bandas)
    
    Returns:
        DataFrame con nuevas columnas para las bandas y métricas relacionadas.
    
    Ejemplo:
        >>> df = calculate_bollinger_bands(df, period=20, std_dev=2)
        >>> df['BB_20_Upper']  # Banda superior
        >>> df['BB_20_Middle']  # Banda media
        >>> df['BB_20_Lower']  # Banda inferior
        >>> df['BB_20_PercentB']  # Porcentaje B (0-1)
    """
    df = df.copy()
    
    # Normalizar nombre de columna
    column = column.lower()
    if column not in df.columns:
        raise ValueError(f"Columna '{column}' no encontrada en el DataFrame")
    
    # Prefijo de salida
    if output_prefix is None:
        output_prefix = f'BB_{period}'
    
    # Calcular SMA (banda media)
    sma = df[column].rolling(window=period, min_periods=1).mean()
    
    # Calcular desviación estándar
    std = df[column].rolling(window=period, min_periods=1).std()
    
    # Calcular bandas
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    
    # Calcular ancho de las bandas
    band_width = upper_band - lower_band
    
    # Calcular Percent B (posición del precio relativo a las bandas)
    # 0 = precio en banda inferior, 1 = precio en banda superior
    percent_b = (df[column] - lower_band) / (upper_band - lower_band)
    percent_b = percent_b.replace([np.inf, -np.inf], np.nan)
    
    # Añadir al DataFrame
    df[f'{output_prefix}_Upper'] = upper_band
    df[f'{output_prefix}_Middle'] = sma
    df[f'{output_prefix}_Lower'] = lower_band
    df[f'{output_prefix}_Width'] = band_width
    df[f'{output_prefix}_PercentB'] = percent_b
    
    return df
