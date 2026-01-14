"""
Indicadores de Volumen

Este módulo contiene indicadores técnicos que analizan el volumen
de trading y su relación con el precio.

Indicadores implementados:
- Volume: Análisis básico de volumen
- VWAP: Volume Weighted Average Price
- MFI: Money Flow Index
- Market Profile: Perfil de mercado (distribución de precio-tiempo)
- Volume Profile: Perfil de volumen (distribución de precio-volumen)
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


def calculate_market_profile(df: pd.DataFrame,
                            bins: int = 30,
                            output_prefix: str = 'Market_Profile') -> pd.DataFrame:
    """
    Calcula el Market Profile básico (distribución precio-tiempo).
    
    El Market Profile muestra cómo se distribuye el precio a lo largo del tiempo,
    identificando áreas de alta y baja actividad (POC - Point of Control,
    Value Area).
    
    NOTA: Esta es una implementación simplificada. El Market Profile completo
    requiere análisis de TPOs (Time Price Opportunities) y sesiones de trading.
    
    Esta implementación calcula:
    - Distribución de precios en bins
    - POC (Point of Control): Precio con mayor frecuencia
    - Value Area: Rango de precios que contiene el 70% del volumen
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columna 'close'.
            El índice debe ser DatetimeIndex para análisis temporal.
        bins: Número de bins para la distribución (default: 30).
        output_prefix: Prefijo para las columnas de salida (default: 'Market_Profile').
            Se crearán:
            - {prefix}_POC: Point of Control (precio más frecuente)
            - {prefix}_Value_High: Parte superior del Value Area
            - {prefix}_Value_Low: Parte inferior del Value Area
    
    Returns:
        DataFrame con nuevas columnas para Market Profile.
    
    Ejemplo:
        >>> df = calculate_market_profile(df)
        >>> df['Market_Profile_POC']  # Point of Control
    """
    df = df.copy()
    
    # Validar columna de cierre
    if 'close' not in df.columns:
        raise ValueError("Columna 'close' no encontrada en el DataFrame")
    
    # Calcular distribución de precios usando histograma
    price_min = df['close'].min()
    price_max = df['close'].max()
    price_range = price_max - price_min
    
    if price_range == 0:
        # Todos los precios son iguales
        df[f'{output_prefix}_POC'] = df['close'].iloc[0]
        df[f'{output_prefix}_Value_High'] = df['close'].iloc[0]
        df[f'{output_prefix}_Value_Low'] = df['close'].iloc[0]
        return df
    
    # Crear bins
    bin_edges = np.linspace(price_min, price_max, bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Calcular frecuencia por bin (usando ventana móvil)
    window_size = min(20, len(df) // 2)  # Ventana adaptativa
    
    poc_values = []
    value_high_values = []
    value_low_values = []
    
    for i in range(len(df)):
        if i < window_size:
            window_data = df['close'].iloc[:i+1]
        else:
            window_data = df['close'].iloc[i-window_size+1:i+1]
        
        # Histograma de la ventana
        hist, _ = np.histogram(window_data, bins=bin_edges)
        
        # POC: bin con mayor frecuencia
        max_idx = np.argmax(hist)
        poc = bin_centers[max_idx]
        
        # Value Area: 70% del volumen
        total_volume = hist.sum()
        if total_volume > 0:
            target_volume = total_volume * 0.70
            cumsum = np.cumsum(hist)
            value_area_mask = cumsum <= target_volume
            
            if value_area_mask.any():
                value_indices = np.where(value_area_mask)[0]
                value_low = bin_centers[value_indices[0]]
                value_high = bin_centers[value_indices[-1]]
            else:
                value_low = poc
                value_high = poc
        else:
            value_low = poc
            value_high = poc
        
        poc_values.append(poc)
        value_high_values.append(value_high)
        value_low_values.append(value_low)
    
    # Añadir al DataFrame
    df[f'{output_prefix}_POC'] = poc_values
    df[f'{output_prefix}_Value_High'] = value_high_values
    df[f'{output_prefix}_Value_Low'] = value_low_values
    
    return df


def calculate_volume_profile(df: pd.DataFrame,
                            bins: int = 30,
                            output_prefix: str = 'Volume_Profile') -> pd.DataFrame:
    """
    Calcula el Volume Profile (distribución precio-volumen).
    
    El Volume Profile muestra cómo se distribuye el volumen a través
    de diferentes niveles de precio, identificando áreas de alta y baja
    actividad de volumen.
    
    Conceptos clave:
    - POC (Point of Control): Nivel de precio con mayor volumen
    - Value Area: Rango de precios que contiene el 70% del volumen
    - High Volume Nodes: Áreas de alta actividad (soportes/resistencias)
    - Low Volume Nodes: Áreas de baja actividad (zonas de ruptura)
    
    Args:
        df: DataFrame con datos OHLCV. Debe tener columnas 'high', 'low', 'close', 'volume'.
        bins: Número de bins para la distribución de precios (default: 30).
        output_prefix: Prefijo para las columnas de salida (default: 'Volume_Profile').
            Se crearán:
            - {prefix}_POC: Point of Control (precio con mayor volumen)
            - {prefix}_Value_High: Parte superior del Value Area
            - {prefix}_Value_Low: Parte inferior del Value Area
            - {prefix}_Volume_Density: Densidad de volumen normalizada
    
    Returns:
        DataFrame con nuevas columnas para Volume Profile.
    
    Ejemplo:
        >>> df = calculate_volume_profile(df)
        >>> df['Volume_Profile_POC']  # Point of Control
    """
    df = df.copy()
    
    # Validar columnas requeridas
    required_cols = ['high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")
    
    # Calcular rango de precios
    price_min = df[['high', 'low']].min().min()
    price_max = df[['high', 'low']].max().max()
    price_range = price_max - price_min
    
    if price_range == 0:
        # Todos los precios son iguales
        df[f'{output_prefix}_POC'] = df['close'].iloc[0]
        df[f'{output_prefix}_Value_High'] = df['close'].iloc[0]
        df[f'{output_prefix}_Value_Low'] = df['close'].iloc[0]
        df[f'{output_prefix}_Volume_Density'] = 1.0
        return df
    
    # Crear bins
    bin_edges = np.linspace(price_min, price_max, bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Calcular Volume Profile usando ventana móvil
    window_size = min(20, len(df) // 2)  # Ventana adaptativa
    
    poc_values = []
    value_high_values = []
    value_low_values = []
    density_values = []
    
    for i in range(len(df)):
        if i < window_size:
            window_data = df.iloc[:i+1]
        else:
            window_data = df.iloc[i-window_size+1:i+1]
        
        # Distribuir volumen por bins según precio típico
        typical_prices = (window_data['high'] + window_data['low'] + window_data['close']) / 3
        volumes = window_data['volume'].values
        
        # Crear histograma ponderado por volumen
        volume_profile, _ = np.histogram(typical_prices, bins=bin_edges, weights=volumes)
        
        # POC: bin con mayor volumen
        max_idx = np.argmax(volume_profile)
        poc = bin_centers[max_idx]
        
        # Value Area: 70% del volumen total
        total_volume = volume_profile.sum()
        if total_volume > 0:
            target_volume = total_volume * 0.70
            cumsum = np.cumsum(volume_profile)
            value_area_mask = cumsum <= target_volume
            
            if value_area_mask.any():
                value_indices = np.where(value_area_mask)[0]
                value_low = bin_centers[value_indices[0]]
                value_high = bin_centers[value_indices[-1]]
            else:
                value_low = poc
                value_high = poc
            
            # Densidad de volumen normalizada para el precio actual
            current_price = df['close'].iloc[i]
            price_bin_idx = np.digitize(current_price, bin_edges) - 1
            price_bin_idx = max(0, min(price_bin_idx, len(volume_profile) - 1))
            density = volume_profile[price_bin_idx] / total_volume if total_volume > 0 else 0
        else:
            value_low = poc
            value_high = poc
            density = 0
        
        poc_values.append(poc)
        value_high_values.append(value_high)
        value_low_values.append(value_low)
        density_values.append(density)
    
    # Añadir al DataFrame
    df[f'{output_prefix}_POC'] = poc_values
    df[f'{output_prefix}_Value_High'] = value_high_values
    df[f'{output_prefix}_Value_Low'] = value_low_values
    df[f'{output_prefix}_Volume_Density'] = density_values
    
    return df
