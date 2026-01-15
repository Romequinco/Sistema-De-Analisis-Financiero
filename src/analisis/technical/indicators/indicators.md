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
