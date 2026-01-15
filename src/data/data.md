# Modulo de Datos

## Objetivo
Extraer y preparar datos financieros para el pipeline.

## Que hace
| Aspecto | Descripcion |
| --- | --- |
| Entradas | Simbolo, periodo, intervalo |
| Salidas | Datos crudos y limpios |
| Estado | Implementado |

## Componentes clave
- `raw/` extraccion y cache
- `cleaning/` limpieza y normalizacion

## Funciones clave (resumen)
| Funcion | Descripcion |
| --- | --- |
| `DataProvider.*` | Extraccion y cache |
| `DataCleaner.*` | Limpieza y validacion |

## Flujo
```mermaid
flowchart LR
    A[Raw] --> B[Cleaning] --> C[Analisis]
```

## Referencias
- Extraccion: `raw/data.md`
- Limpieza: `cleaning/cleaning.md`
