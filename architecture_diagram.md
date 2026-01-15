# Diagrama de Arquitectura

## Objetivo
Vista unica del pipeline y dependencias entre modulos.

## Flujo
```mermaid
flowchart TD
    A[Data/raw] --> B[Data/cleaning]
    B --> C[Analisis tecnico]
    B --> D[Analisis fundamental]
    C --> E[Scoring]
    D --> E
    E --> F[Decision]
    F --> G[Visualizacion]
```

## Referencias
- Detalle por modulo: `README.md`
