"""
Wyckoff (Experimental)
"""

import pandas as pd


def identify_wyckoff_phases(df: pd.DataFrame,
                            output_column: str = 'Wyckoff_Phase') -> pd.DataFrame:
    """
    Identifica fases Wyckoff de forma heuristica (experimental, no pipeline).
    """
    df = df.copy()

    required_cols = ['high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no encontrada en el DataFrame")

    df['price_change'] = df['close'].pct_change()
    df['volume_avg'] = df['volume'].rolling(window=20, min_periods=1).mean()
    df['volume_ratio'] = df['volume'] / df['volume_avg']

    high_low = df['high'] - df['low']
    df['volatility'] = high_low.rolling(window=14, min_periods=1).mean()
    df['volatility_avg'] = df['volatility'].rolling(window=20, min_periods=1).mean()
    df['volatility_ratio'] = df['volatility'] / df['volatility_avg']

    phases = []
    for i in range(len(df)):
        if i < 20:
            phases.append('Unknown')
            continue

        price_change = df['price_change'].iloc[i]
        volume_ratio = df['volume_ratio'].iloc[i]
        volatility_ratio = df['volatility_ratio'].iloc[i]

        if price_change > 0.01 and volume_ratio > 1.2 and volatility_ratio < 1.0:
            phases.append('Markup')
        elif price_change < -0.01 and volume_ratio > 1.2 and volatility_ratio < 1.0:
            phases.append('Markdown')
        elif abs(price_change) < 0.005 and volume_ratio > 1.1 and volatility_ratio < 0.9:
            phases.append('Accumulation')
        elif abs(price_change) < 0.005 and volume_ratio > 1.1 and volatility_ratio < 0.9:
            phases.append('Distribution')
        else:
            phases.append('Unknown')

    df[output_column] = phases
    df = df.drop(columns=['price_change', 'volume_avg', 'volume_ratio',
                          'volatility', 'volatility_avg', 'volatility_ratio'])
    return df
