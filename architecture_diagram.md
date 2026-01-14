# [DIAGRAMA] Diagrama Conceptual del Sistema

```mermaid
flowchart TD

A[Usuario / Configuración] --> B[Data Provider<br/>src/data/raw/]
B --> C[Cache / Almacenamiento Local]

C --> D1[Data Cleaner<br/>src/data/cleaning/]
D1 --> D2[Datos Limpios]

D2 --> E[Análisis Técnico<br/>src/analisis/technical/]
D2 --> F[Análisis Fundamental<br/>src/analisis/fundamental/]

E --> E1[Indicadores Técnicos]
E --> E2[Estrategias Técnicas]

F --> F1[Value Investing]
F --> F2[Growth Investing]
F --> F3[Quality Investing]
F --> F4[Health Analysis]
F --> F5[Estrategias Mixtas]

E1 --> G[Scoring Engine<br/>src/analisis/scoring/]
E2 --> G
F1 --> G
F2 --> G
F3 --> G
F4 --> G
F5 --> G

G --> H[Decision Engine<br/>src/final/decision/]

H --> H1[Score Numérico]
H --> H2[Clasificación]
H --> H3[Explicación]

H1 --> I[Visualización<br/>src/final/visualization/]
H2 --> I
H3 --> I

I --> J[Reporte Final]

style B fill:#4472C4,stroke:#333,stroke-width:2px,color:#fff
style D1 fill:#70AD47,stroke:#333,stroke-width:2px,color:#fff
style E fill:#FFC000,stroke:#333,stroke-width:2px,color:#fff
style F fill:#FFC000,stroke:#333,stroke-width:2px,color:#fff
style G fill:#7030A0,stroke:#333,stroke-width:2px,color:#fff
style H fill:#C00000,stroke:#333,stroke-width:2px,color:#fff
style I fill:#0070C0,stroke:#333,stroke-width:2px,color:#fff
```

---

## [DESCRIPCION] Descripción del flujo

### Fase 1: Datos (`src/data/`)
- **Data Provider** (`raw/`): abstrae la fuente de datos (IMPLEMENTADO con yfinance)
- **Cache**: evita llamadas innecesarias (IMPLEMENTADO con TTL y reintentos)
- **Data Cleaner** (`cleaning/`): limpia y preprocesa datos (IMPLEMENTADO)

### Fase 2: Análisis (`src/analisis/`)
- **Análisis Técnico** (`technical/`): genera señales técnicas (PENDIENTE)
- **Análisis Fundamental** (`fundamental/`): genera señales fundamentales (PENDIENTE)
- **Scoring Engine** (`scoring/`): normaliza y pondera señales (PENDIENTE)

### Fase 3: Final (`src/final/`)
- **Decision Engine** (`decision/`): clasifica y explica (PENDIENTE)
- **Visualización** (`visualization/`): gráficos y tablas ejecutivas (PARCIAL - tablas implementadas)

## [ESTADO] Estado de Implementación

### [COMPLETADO]
- Data Provider (`src/data/raw/`) con cache y manejo de errores
- Data Cleaner (`src/data/cleaning/`) para limpieza y preprocesamiento
- Funciones de visualización básicas (tablas)

### [PENDIENTE]
- Análisis técnico (`src/analisis/technical/`)
- Análisis fundamental (`src/analisis/fundamental/`)
- Sistema de scoring (`src/analisis/scoring/`)
- Motor de decisión (`src/final/decision/`)
- Visualización avanzada (`src/final/visualization/`)

## [ESTRUCTURA] Nueva Estructura del Proyecto

```
src/
├── data/           Datos (extracción y limpieza)
├── analisis/       Análisis (técnico, fundamental, scoring)
├── final/          Final (decisión, visualización)
├── config/         Configuración
└── utils/          Utilidades
```
