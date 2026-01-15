"""
Parabolic SAR (Experimental)
"""

import numpy as np
import pandas as pd


def calculate_parabolic_sar(df: pd.DataFrame,
                            af_start: float = 0.02,
                            af_increment: float = 0.02,
                            af_max: float = 0.2,
                            output_column: str = 'Parabolic_SAR') -> pd.DataFrame:
    """
    Calcula el Parabolic SAR (experimental, no pipeline).
    """
    df = df.copy()

    required_cols = ['high', 'low', 'close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")

    high = df['high'].values
    low = df['low'].values
    sar = np.zeros(len(df))
    trend = np.zeros(len(df), dtype=int)
    ep = np.zeros(len(df))
    af = np.zeros(len(df))

    sar[0] = low[0]
    trend[0] = 1
    ep[0] = high[0]
    af[0] = af_start

    for i in range(1, len(df)):
        sar_prev = sar[i - 1]
        trend_prev = trend[i - 1]
        ep_prev = ep[i - 1]
        af_prev = af[i - 1]

        if trend_prev == 1:
            sar[i] = sar_prev + af_prev * (ep_prev - sar_prev)
            sar[i] = min(sar[i], low[i - 1], low[i])
            if high[i] > ep_prev:
                ep[i] = high[i]
                af[i] = min(af_prev + af_increment, af_max)
            else:
                ep[i] = ep_prev
                af[i] = af_prev
            if low[i] < sar[i]:
                trend[i] = -1
                sar[i] = ep_prev
                ep[i] = low[i]
                af[i] = af_start
            else:
                trend[i] = 1
        else:
            sar[i] = sar_prev + af_prev * (ep_prev - sar_prev)
            sar[i] = max(sar[i], high[i - 1], high[i])
            if low[i] < ep_prev:
                ep[i] = low[i]
                af[i] = min(af_prev + af_increment, af_max)
            else:
                ep[i] = ep_prev
                af[i] = af_prev
            if high[i] > sar[i]:
                trend[i] = 1
                sar[i] = ep_prev
                ep[i] = high[i]
                af[i] = af_start
            else:
                trend[i] = -1

    df[output_column] = sar
    return df
