# Indicadores Tecnicos Basicos

## Objetivo
Catalogo de indicadores basicos disponibles y sus parametros clave.

## Que hace
| Aspecto | Descripcion |
| --- | --- |
| Entradas | DataFrame OHLCV limpio |
| Salidas | Columnas de indicadores por categoria |
| Alcance | Tendencia, momentum, volatilidad, volumen, price action |

## Componentes clave
- `trend.py`
- `momentum.py`
- `volatility.py`
- `volume.py`
- `price_action.py`

## Funciones clave (resumen)
| Archivo | Funciones |
| --- | --- |
| `trend.py` | `calculate_sma`, `calculate_ema`, `calculate_hma`, `calculate_sma_series`, `calculate_ema_series` |
| `momentum.py` | `calculate_rsi`, `calculate_adx`, `calculate_stochastic_rsi` |
| `volatility.py` | `calculate_atr`, `calculate_bollinger_bands` |
| `volume.py` | `calculate_volume_indicators`, `calculate_vwap`, `calculate_mfi`, `calculate_ad` |
| `price_action.py` | `calculate_fractals`, `calculate_support_resistance`, `calculate_pivot_points` |

## Indicadores (resumen)
| Categoria | Indicadores | Parametros relevantes |
| --- | --- | --- |
| Tendencia | SMA, EMA, HMA | SMA/EMA 8, 18, 40; HMA 20 |
| Momentum | RSI, ADX, Stoch RSI | RSI 14 (30/50/70), ADX 14 (20-25), Stoch 14 (K/D 3/3) |
| Volatilidad | ATR, Bollinger Bands | ATR 14, BB 20/2.0 |
| Volumen | Volume SMA, VWAP, MFI, A/D | MFI 14 (20/80) |
| Price action | Fractales, Support/Resistance, Pivots | Swings, PP/R1/R2/S1/S2 |

## Inputs / Outputs
| Tipo | Descripcion |
| --- | --- |
| Inputs | `open/high/low/close/volume` |
| Outputs | Columnas nuevas por indicador |

## Notas
- Este modulo no genera señales ni estrategias.
- HMA 20: compromiso entre rapidez y ruido.
- Experimental: Parabolic SAR, Wyckoff, Market Profile, Volume Profile.
- Indicadores experimentales: `../experimental/experimental.md`
