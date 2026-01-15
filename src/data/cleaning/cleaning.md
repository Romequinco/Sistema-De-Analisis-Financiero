# Modulo de Limpieza de Datos

## Objetivo
Normalizar y validar datos financieros antes del analisis.

## Que hace
| Aspecto | Descripcion |
| --- | --- |
| Entradas | Precios, fundamentales, estados financieros |
| Salidas | Datos limpios + metadata |
| Estado | Implementado |

## Procesos clave
- Normalizacion de columnas e indices
- Validacion OHLC
- Manejo de nulos y duplicados
- Outliers (deteccion opcional)
- Columnas derivadas (returns, volatilidad)

## Inputs / Outputs
| Tipo | Descripcion |
| --- | --- |
| Inputs | DataFrames crudos |
| Outputs | DataFrames limpios + `CleaningMetadata` |

## Notas / Limitaciones
- No descarga datos (solo limpia).
- La limpieza es conservadora.
