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
| `trend.py` | `calculate_sma`, `calculate_ema`, `calculate_sma_series`, `calculate_ema_series`, `calculate_parabolic_sar` |
| `momentum.py` | `calculate_rsi`, `calculate_adx`, `calculate_stochastic_rsi` |
| `volatility.py` | `calculate_atr`, `calculate_bollinger_bands` |
| `volume.py` | `calculate_volume_indicators`, `calculate_vwap`, `calculate_mfi`, `calculate_market_profile`, `calculate_volume_profile` |
| `price_action.py` | `calculate_fractals`, `identify_wyckoff_phases` |

## Indicadores (resumen)
| Categoria | Indicadores | Parametros relevantes |
| --- | --- | --- |
| Tendencia | SMA, EMA, Parabolic SAR | SMA/EMA 8, 18, 40 |
| Momentum | RSI, ADX, Stoch RSI | RSI 14 (umbrales 30/70) |
| Volatilidad | ATR, Bollinger Bands | ATR 14, BB 20/2.0 |
| Volumen | Volume SMA, VWAP, MFI | MFI 14 (umbrales 20/80) |
| Price action | Fractales, Wyckoff | Parametros propios |

## Inputs / Outputs
| Tipo | Descripcion |
| --- | --- |
| Inputs | `open/high/low/close/volume` |
| Outputs | Columnas nuevas por indicador |

## Notas
- Este modulo no genera señales ni estrategias.
