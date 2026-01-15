# Modulo de Analisis Tecnico

## Objetivo
Calcular indicadores tecnicos sobre datos limpios. No genera señales ni estrategias.

## Que hace
| Aspecto | Descripcion |
| --- | --- |
| Entradas | DataFrame OHLCV limpio |
| Salidas | DataFrame con columnas de indicadores |
| Estado | Parcial (indicadores base) |

## Componentes clave
- `indicators/` indicadores basicos por categoria
- `composite_indicators/` indicadores compuestos

## Funciones clave (resumen)
| Fuente | Funcion |
| --- | --- |
| Basicos | Ver `indicators/indicators.md` |
| Compuestos | Ver `composite_indicators/composite_indicators.md` |

## Referencias
- Indicadores basicos: `indicators/indicators.md`
- Indicadores compuestos: `composite_indicators/composite_indicators.md`
- Ejemplos: `notebooks/indicators_test.ipynb`
