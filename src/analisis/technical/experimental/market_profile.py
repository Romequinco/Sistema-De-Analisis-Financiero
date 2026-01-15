"""
Market Profile (Experimental)
"""

import numpy as np
import pandas as pd


def calculate_market_profile(df: pd.DataFrame,
                             bins: int = 30,
                             output_prefix: str = 'Market_Profile') -> pd.DataFrame:
    """
    Market Profile simplificado (experimental, no pipeline).
    """
    df = df.copy()

    if 'close' not in df.columns:
        raise ValueError("Columna 'close' no encontrada en el DataFrame")

    price_min = df['close'].min()
    price_max = df['close'].max()
    price_range = price_max - price_min

    if price_range == 0:
        df[f'{output_prefix}_POC'] = df['close'].iloc[0]
        df[f'{output_prefix}_Value_High'] = df['close'].iloc[0]
        df[f'{output_prefix}_Value_Low'] = df['close'].iloc[0]
        return df

    bin_edges = np.linspace(price_min, price_max, bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    window_size = min(20, len(df) // 2)
    poc_values = []
    value_high_values = []
    value_low_values = []

    for i in range(len(df)):
        window_data = df['close'].iloc[:i + 1] if i < window_size else df['close'].iloc[i - window_size + 1:i + 1]
        hist, _ = np.histogram(window_data, bins=bin_edges)
        max_idx = np.argmax(hist)
        poc = bin_centers[max_idx]

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

    df[f'{output_prefix}_POC'] = poc_values
    df[f'{output_prefix}_Value_High'] = value_high_values
    df[f'{output_prefix}_Value_Low'] = value_low_values

    return df
