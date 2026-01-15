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
- `experimental/` indicadores exploratorios (fuera del pipeline)

## Funciones clave (resumen)
| Fuente | Funcion |
| --- | --- |
| Basicos | Ver `indicators/indicators.md` |
| Compuestos | Ver `composite_indicators/composite_indicators.md` |
| Experimental | No se usa en pipeline ni scoring |

## Referencias
- Indicadores basicos: `indicators/indicators.md`
- Indicadores compuestos: `composite_indicators/composite_indicators.md`
- Experimental: `experimental/experimental.md`
- Ejemplos: `notebooks/indicators_test.ipynb`
