"""
Indicadores de Volumen

Este módulo contiene indicadores técnicos que analizan el volumen
de trading y su relación con el precio.

Indicadores implementados:
- Volume: Análisis básico de volumen
- VWAP: Volume Weighted Average Price
- MFI: Money Flow Index
- A/D: Accumulation/Distribution Line
"""

import pandas as pd
import numpy as np
from typing import Optional


def calculate_volume_indicators(df: pd.DataFrame,
                               output_prefix: str = 'Volume') -> pd.DataFrame:
    """
    Calcula indicadores básicos de volumen.
    
    Añade columnas derivadas del volumen para análisis:
    - Volume SMA: Media móvil simple del volumen
    - Volume Ratio: Ratio entre volumen actual y volumen promedio
    - Volume Change: Cambio porcentual del volumen
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'volume'.
        output_prefix: Prefijo para las columnas de salida (default: 'Volume').
            Se crearán:
            - {prefix}_SMA_20: Media móvil de 20 períodos
            - {prefix}_Ratio: Ratio volumen actual / volumen promedio
            - {prefix}_Change: Cambio porcentual del volumen
    
    Returns:
        DataFrame con nuevas columnas de indicadores de volumen.
    
    Ejemplo:
        >>> df = calculate_volume_indicators(df)
        >>> df['Volume_SMA_20']  # Media móvil del volumen
        >>> df['Volume_Ratio']  # Ratio de volumen
    """
    df = df.copy()
    
    # Validar columna de volumen
    if 'volume' not in df.columns:
        raise ValueError("Columna 'volume' no encontrada en el DataFrame")
    
    # Calcular SMA del volumen (20 períodos)
    df[f'{output_prefix}_SMA_20'] = df['volume'].rolling(window=20, min_periods=1).mean()
    
    # Calcular ratio de volumen (volumen actual / volumen promedio)
    df[f'{output_prefix}_Ratio'] = df['volume'] / df[f'{output_prefix}_SMA_20']
    
    # Calcular cambio porcentual del volumen
    df[f'{output_prefix}_Change'] = df['volume'].pct_change()
    
    return df


def calculate_vwap(df: pd.DataFrame,
                  output_column: str = 'VWAP') -> pd.DataFrame:
    """
    Calcula el Volume Weighted Average Price (VWAP).
    
    El VWAP es el precio promedio ponderado por volumen durante un período.
    Se recalcula cada día usando datos desde el inicio del día.
    
    El VWAP es ampliamente usado como referencia de precio "justo" y
    como nivel de soporte/resistencia dinámico.
    
    Interpretación:
    - Precio por encima de VWAP: Sentimiento alcista
    - Precio por debajo de VWAP: Sentimiento bajista
    - VWAP actúa como soporte/resistencia dinámico
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close', 'volume'.
            El índice debe ser DatetimeIndex para calcular VWAP diario.
        output_column: Nombre de la columna de salida (default: 'VWAP').
    
    Returns:
        DataFrame con una nueva columna 'VWAP'.
    
    Ejemplo:
        >>> df = calculate_vwap(df)
        >>> df['VWAP']  # Acceder al VWAP
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    # Verificar que el índice sea DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("El índice del DataFrame debe ser DatetimeIndex para calcular VWAP diario")
    
    # Calcular precio típico (Typical Price)
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    
    # Calcular PV (Price × Volume)
    pv = typical_price * df['volume']
    
    # Calcular VWAP por día
    df['date'] = df.index.date
    vwap = pv.groupby(df['date']).cumsum() / df['volume'].groupby(df['date']).cumsum()
    
    # Añadir al DataFrame
    df[output_column] = vwap
    
    # Eliminar columna temporal
    df = df.drop(columns=['date'])
    
    return df


def calculate_mfi(df: pd.DataFrame,
                 period: int = 14,
                 output_column: Optional[str] = None) -> pd.DataFrame:
    """
    Calcula el Money Flow Index (MFI).
    
    El MFI es similar al RSI pero incorpora volumen. Combina precio y volumen
    para medir la fuerza del dinero que fluye hacia o desde un activo.
    
    Interpretación:
    - MFI > 80: Sobrecompra (posible señal de venta)
    - MFI < 20: Sobreventa (posible señal de compra)
    - MFI entre 20-80: Zona neutral
    
    El MFI se calcula como:
    1. Calcular Raw Money Flow = Typical Price × Volume
    2. Separar Positive Money Flow y Negative Money Flow
    3. Calcular Money Ratio = Positive MF / Negative MF
    4. MFI = 100 - (100 / (1 + Money Ratio))
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close', 'volume'.
        period: Período para el cálculo (default: 14).
        output_column: Nombre de la columna de salida. Si es None, usa 'MFI_{period}'.
    
    Returns:
        DataFrame con una nueva columna 'MFI_{period}' o el nombre especificado.
    
    Ejemplo:
        >>> df = calculate_mfi(df, period=14)
        >>> df['MFI_14']  # Acceder al MFI de 14 períodos
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    # Nombre de columna de salida
    if output_column is None:
        output_column = f'MFI_{period}'
    
    # Calcular Typical Price
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    
    # Calcular Raw Money Flow
    raw_money_flow = typical_price * df['volume']
    
    # Calcular cambios en Typical Price
    tp_change = typical_price.diff()
    
    # Separar Positive y Negative Money Flow
    positive_mf = raw_money_flow.where(tp_change > 0, 0)
    negative_mf = raw_money_flow.where(tp_change < 0, 0)
    
    # Calcular promedio de Positive y Negative MF usando método Wilder
    # Primera iteración: promedio simple
    positive_mf_avg = positive_mf.rolling(window=period, min_periods=period).mean()
    negative_mf_avg = negative_mf.rolling(window=period, min_periods=period).mean()
    
    # Iteraciones siguientes: promedio exponencial (método Wilder)
    for i in range(period, len(df)):
        if i == period:
            continue
        positive_mf_avg.iloc[i] = (positive_mf_avg.iloc[i-1] * (period - 1) + positive_mf.iloc[i]) / period
        negative_mf_avg.iloc[i] = (negative_mf_avg.iloc[i-1] * (period - 1) + negative_mf.iloc[i]) / period
    
    # Calcular Money Ratio
    money_ratio = positive_mf_avg / negative_mf_avg
    
    # Calcular MFI
    mfi = 100 - (100 / (1 + money_ratio))
    
    # Añadir al DataFrame
    df[output_column] = mfi
    
    return df


def calculate_ad(df: pd.DataFrame,
                 output_column: str = 'AD') -> pd.DataFrame:
    """
    Calcula Accumulation/Distribution Line (A/D).

    Implementación clásica sin parámetros libres.
    """
    df = df.copy()

    required_cols = ['high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")

    high = df['high']
    low = df['low']
    close = df['close']
    volume = df['volume']

    price_range = (high - low).replace(0, np.nan)
    mfm = ((close - low) - (high - close)) / price_range
    mfm = mfm.fillna(0.0)
    mfv = mfm * volume

    df[output_column] = mfv.cumsum()

    return df
