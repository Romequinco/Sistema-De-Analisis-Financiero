# Modulo de Scoring

## Objetivo
Agregar señales tecnicas y fundamentales en un score unico.

## Que hace
| Aspecto | Descripcion |
| --- | --- |
| Entradas | Señales normalizadas por estrategia |
| Salidas | Score total, clasificacion, breakdown |
| Estado | Pendiente de implementacion |

## Flujo
```mermaid
flowchart TD
    A[Señales] --> B[Estrategias]
    B --> C[Bloques]
    C --> D[Score total]
    D --> E[Clasificacion]
```

## Componentes clave
- Normalizacion y validacion de señales
- Agregacion por estrategia y bloque
- Pesos configurables

## Referencias
- Diseño completo: `scoring_system.md`
