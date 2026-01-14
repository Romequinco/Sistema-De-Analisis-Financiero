"""
Indicadores de Momentum

Este módulo contiene indicadores técnicos que miden la velocidad
y fuerza de los movimientos de precio.

Indicadores implementados:
- RSI: Relative Strength Index
- ADX: Average Directional Index
- Stochastic RSI: Stochastic del RSI
"""

import pandas as pd
import numpy as np
from typing import Optional


def calculate_rsi(df: pd.DataFrame,
                  column: str = 'close',
                  period: int = 14,
                  output_column: Optional[str] = None) -> pd.DataFrame:
    """
    Calcula el Relative Strength Index (RSI).
    
    El RSI es un oscilador de momentum que mide la velocidad y magnitud
    de los cambios de precio. Oscila entre 0 y 100.
    
    Interpretación clásica:
    - RSI > 70: Sobrecompra (posible señal de venta)
    - RSI < 30: Sobreventa (posible señal de compra)
    - RSI entre 30-70: Zona neutral
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'close' o la especificada.
        column: Nombre de la columna de precio a usar (default: 'close').
        period: Período para el cálculo (default: 14).
        output_column: Nombre de la columna de salida. Si es None, usa 'RSI_{period}'.
    
    Returns:
        DataFrame con una nueva columna 'RSI_{period}' o el nombre especificado.
    
    Ejemplo:
        >>> df = calculate_rsi(df, period=14)
        >>> df['RSI_14']  # Acceder al RSI de 14 períodos
    """
    df = df.copy()
    
    # Normalizar nombre de columna
    column = column.lower()
    if column not in df.columns:
        raise ValueError(f"Columna '{column}' no encontrada en el DataFrame")
    
    # Nombre de columna de salida
    if output_column is None:
        output_column = f'RSI_{period}'
    
    # Calcular cambios de precio
    delta = df[column].diff()
    
    # Separar ganancias y pérdidas
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calcular promedio de ganancias y pérdidas usando método Wilder
    # Primera iteración: promedio simple
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    
    # Iteraciones siguientes: promedio exponencial (método Wilder)
    for i in range(period, len(df)):
        if i == period:
            continue
        avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (period - 1) + loss.iloc[i]) / period
    
    # Calcular RS y RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # Añadir al DataFrame
    df[output_column] = rsi
    
    return df


def calculate_adx(df: pd.DataFrame,
                  period: int = 14,
                  output_column: str = 'ADX') -> pd.DataFrame:
    """
    Calcula el Average Directional Index (ADX).
    
    El ADX mide la fuerza de una tendencia, no su dirección.
    Valores altos indican una tendencia fuerte, valores bajos indican
    un mercado sin tendencia (lateral).
    
    Interpretación:
    - ADX > 25: Tendencia fuerte
    - ADX 20-25: Tendencia moderada
    - ADX < 20: Mercado sin tendencia (lateral)
    
    El ADX se calcula a partir de:
    - +DI: Directional Indicator positivo (tendencia alcista)
    - -DI: Directional Indicator negativo (tendencia bajista)
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close'.
        period: Período para el cálculo (default: 14).
        output_column: Nombre base para las columnas de salida. Se crearán:
            - {output_column}: ADX
            - {output_column}_Plus_DI: +DI
            - {output_column}_Minus_DI: -DI
    
    Returns:
        DataFrame con nuevas columnas 'ADX', 'ADX_Plus_DI', 'ADX_Minus_DI'.
    
    Ejemplo:
        >>> df = calculate_adx(df)
        >>> df['ADX']  # Fuerza de la tendencia
        >>> df['ADX_Plus_DI']  # Indicador direccional positivo
        >>> df['ADX_Minus_DI']  # Indicador direccional negativo
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
    
    # Calcular True Range (TR)
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
    
    # Calcular Directional Movement
    plus_dm = []
    minus_dm = []
    
    for i in range(len(df)):
        if i == 0:
            plus_dm.append(0)
            minus_dm.append(0)
        else:
            up_move = high[i] - high[i-1]
            down_move = low[i-1] - low[i]
            
            if up_move > down_move and up_move > 0:
                plus_dm.append(up_move)
            else:
                plus_dm.append(0)
            
            if down_move > up_move and down_move > 0:
                minus_dm.append(down_move)
            else:
                minus_dm.append(0)
    
    # Calcular promedio de TR, +DM, -DM (método Wilder)
    tr_series = pd.Series(tr_list)
    plus_dm_series = pd.Series(plus_dm)
    minus_dm_series = pd.Series(minus_dm)
    
    # Promedio inicial (simple)
    atr = tr_series.rolling(window=period, min_periods=period).mean()
    plus_di_avg = plus_dm_series.rolling(window=period, min_periods=period).mean()
    minus_di_avg = minus_dm_series.rolling(window=period, min_periods=period).mean()
    
    # Promedio exponencial (método Wilder) para períodos siguientes
    for i in range(period, len(df)):
        if i == period:
            continue
        atr.iloc[i] = (atr.iloc[i-1] * (period - 1) + tr_list[i]) / period
        plus_di_avg.iloc[i] = (plus_di_avg.iloc[i-1] * (period - 1) + plus_dm[i]) / period
        minus_di_avg.iloc[i] = (minus_di_avg.iloc[i-1] * (period - 1) + minus_dm[i]) / period
    
    # Calcular +DI y -DI
    plus_di = 100 * (plus_di_avg / atr)
    minus_di = 100 * (minus_di_avg / atr)
    
    # Calcular DX (Directional Index)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    
    # Calcular ADX (promedio de DX usando método Wilder)
    adx = dx.rolling(window=period, min_periods=period).mean()
    
    # Promedio exponencial para períodos siguientes
    for i in range(period * 2 - 1, len(df)):
        if i == period * 2 - 1:
            continue
        adx.iloc[i] = (adx.iloc[i-1] * (period - 1) + dx.iloc[i]) / period
    
    # Añadir al DataFrame
    df[f'{output_column}'] = adx
    df[f'{output_column}_Plus_DI'] = plus_di
    df[f'{output_column}_Minus_DI'] = minus_di
    
    return df


def calculate_stochastic_rsi(df: pd.DataFrame,
                             rsi_period: int = 14,
                             stoch_period: int = 14,
                             k_period: int = 3,
                             d_period: int = 3,
                             output_column: str = 'Stoch_RSI') -> pd.DataFrame:
    """
    Calcula el Stochastic RSI (StochRSI).
    
    El StochRSI es una versión estocástica del RSI que oscila entre 0 y 1
    (o 0 y 100 si se multiplica por 100). Es más sensible que el RSI
    y puede generar más señales.
    
    Interpretación:
    - StochRSI > 0.8: Sobrecompra extrema
    - StochRSI < 0.2: Sobreventa extrema
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'close'.
        rsi_period: Período para el cálculo del RSI (default: 14).
        stoch_period: Período para el cálculo estocástico (default: 14).
        k_period: Período para la línea %K (default: 3).
        d_period: Período para la línea %D (default: 3).
        output_column: Nombre base para las columnas de salida. Se crearán:
            - {output_column}_K: Línea %K
            - {output_column}_D: Línea %D
    
    Returns:
        DataFrame con nuevas columnas 'Stoch_RSI_K' y 'Stoch_RSI_D'.
    
    Ejemplo:
        >>> df = calculate_stochastic_rsi(df)
        >>> df['Stoch_RSI_K']  # Línea %K
        >>> df['Stoch_RSI_D']  # Línea %D (promedio móvil de %K)
    """
    df = df.copy()
    
    # Primero calcular RSI
    df = calculate_rsi(df, period=rsi_period, output_column='RSI_temp')
    
    # Calcular Stochastic del RSI
    rsi_values = df['RSI_temp'].values
    
    # Calcular %K
    stoch_k = []
    for i in range(len(df)):
        if i < stoch_period - 1:
            stoch_k.append(np.nan)
        else:
            rsi_window = rsi_values[i - stoch_period + 1:i + 1]
            rsi_min = np.nanmin(rsi_window)
            rsi_max = np.nanmax(rsi_window)
            
            if rsi_max == rsi_min:
                stoch_k.append(50)  # Valor neutral si no hay variación
            else:
                stoch_k.append(100 * (rsi_values[i] - rsi_min) / (rsi_max - rsi_min))
    
    # Calcular %D (promedio móvil de %K)
    stoch_k_series = pd.Series(stoch_k)
    stoch_d = stoch_k_series.rolling(window=d_period, min_periods=1).mean()
    
    # Añadir al DataFrame
    df[f'{output_column}_K'] = stoch_k
    df[f'{output_column}_D'] = stoch_d
    
    # Eliminar columna temporal
    df = df.drop(columns=['RSI_temp'])
    
    return df
