# Indicadores Tecnicos Compuestos

## Objetivo
Indicadores compuestos que agregan multiples señales en un solo calculo.

## Que hace
| Aspecto | Descripcion |
| --- | --- |
| Entradas | DataFrame OHLCV limpio |
| Salidas | Columnas de indicadores compuestos |
| Uso | Analisis de tendencia y momentum con menor numero de señales |

## Indicadores disponibles
| Indicador | Proposito | Salidas clave |
| --- | --- | --- |
| MACD | Momentum + tendencia | `MACD_Line`, `MACD_Signal`, `MACD_Histogram` |
| Ichimoku | Tendencia/soporte | Lineas Tenkan/Kijun/Spans |
| SuperTrend | Tendencia adaptativa | Linea y direccion |
| Adaptive MA | Media movil adaptativa | Columna MA adaptativa |

## Funciones clave
| Funcion | Descripcion |
| --- | --- |
| `calculate_macd` | MACD |
| `calculate_ichimoku` | Ichimoku |
| `calculate_supertrend` | SuperTrend |
| `calculate_adaptive_ma` | Adaptive MA |

## Referencias
- Indicadores basicos: `../indicators/indicators.md`
