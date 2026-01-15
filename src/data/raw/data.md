# Data Provider (Yahoo Finance)

## Objetivo
Proveer datos de mercado y fundamentales con cache local.

## Que hace
| Aspecto | Descripcion |
| --- | --- |
| Entradas | Simbolo, periodo, intervalo |
| Salidas | Precios, fundamentales, estados financieros |
| Cache | TTL configurable con fallback |

## Inputs / Outputs
| Tipo | Descripcion |
| --- | --- |
| Inputs | `symbol`, `period`, `interval` |
| Outputs | `price_data`, `fundamental_data`, `financial_statements` |

## Flujo de cache
```mermaid
flowchart TD
    A[Request] --> B{Cache valido?}
    B -- Si --> C[Return cache]
    B -- No --> D[Fetch datos]
    D --> E[Guardar cache]
    E --> C
```

## Notas / Limitaciones
- Fuente: Yahoo Finance (`yfinance`).
- Datos pueden tener retraso.
- Cache es local por proceso.
