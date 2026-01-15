"""
Volume Profile (Experimental)
"""

import numpy as np
import pandas as pd


def calculate_volume_profile(df: pd.DataFrame,
                             bins: int = 30,
                             output_prefix: str = 'Volume_Profile') -> pd.DataFrame:
    """
    Volume Profile simplificado (experimental, no pipeline).
    """
    df = df.copy()

    required_cols = ['high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")

    price_min = df[['high', 'low']].min().min()
    price_max = df[['high', 'low']].max().max()
    price_range = price_max - price_min

    if price_range == 0:
        df[f'{output_prefix}_POC'] = df['close'].iloc[0]
        df[f'{output_prefix}_Value_High'] = df['close'].iloc[0]
        df[f'{output_prefix}_Value_Low'] = df['close'].iloc[0]
        df[f'{output_prefix}_Volume_Density'] = 1.0
        return df

    bin_edges = np.linspace(price_min, price_max, bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    window_size = min(20, len(df) // 2)
    poc_values = []
    value_high_values = []
    value_low_values = []
    density_values = []

    for i in range(len(df)):
        window_data = df.iloc[:i + 1] if i < window_size else df.iloc[i - window_size + 1:i + 1]
        typical_prices = (window_data['high'] + window_data['low'] + window_data['close']) / 3
        volumes = window_data['volume'].values
        volume_profile, _ = np.histogram(typical_prices, bins=bin_edges, weights=volumes)

        max_idx = np.argmax(volume_profile)
        poc = bin_centers[max_idx]

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

    df[f'{output_prefix}_POC'] = poc_values
    df[f'{output_prefix}_Value_High'] = value_high_values
    df[f'{output_prefix}_Value_Low'] = value_low_values
    df[f'{output_prefix}_Volume_Density'] = density_values

    return df
