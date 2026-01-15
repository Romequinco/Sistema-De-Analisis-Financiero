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

## Funciones clave
| Funcion | Descripcion |
| --- | --- |
| `DataCleaner.clean_price_data` | Limpieza OHLCV |
| `DataCleaner.clean_fundamental_data` | Limpieza de fundamentales |
| `DataCleaner.clean_financial_statement` | Limpieza de estados financieros |
| `clean_price_data` | Wrapper rapido de limpieza |
| `clean_fundamental_data` | Wrapper rapido de fundamentales |
| `clean_financial_statement` | Wrapper rapido de estados |
| `CleaningMetadata.summary` | Resumen de limpieza |

## Notas / Limitaciones
- No descarga datos (solo limpia).
- La limpieza es conservadora.
