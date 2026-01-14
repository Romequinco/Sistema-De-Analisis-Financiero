# [VISUALIZATION] Módulo de Visualización y Reporting

## [UBICACION] Ubicación

`src/final/visualization/`

## [OBJETIVO] Objetivo

Este módulo genera **gráficos, tablas y reportes ejecutivos** a partir de los resultados del análisis completo, proporcionando visualizaciones claras y profesionales para la toma de decisiones.

El módulo de visualización:
- Crea gráficos de precios con indicadores técnicos
- Genera tablas ejecutivas con métricas clave
- Visualiza el breakdown del score
- Crea gráficos comparativos
- Genera reportes completos (PDF/HTML)
- Proporciona dashboards interactivos

---

## [ESTADO] Estado Actual

Módulo en desarrollo inicial. Pendiente de implementación.

---

## [ARQUITECTURA] Arquitectura del Módulo

```
VisualizationEngine
├── Price Charts
│   ├── Candlestick Charts
│   ├── Line Charts
│   ├── Volume Charts
│   └── Indicator Overlays
├── Score Visualization
│   ├── Score Breakdown Charts
│   ├── Radar Charts
│   ├── Waterfall Charts
│   └── Comparison Charts
├── Tables
│   ├── Executive Summary Tables
│   ├── Metric Comparison Tables
│   └── Historical Data Tables
├── Reports
│   ├── PDF Reports
│   ├── HTML Reports
│   └── Interactive Dashboards
└── Styling
    ├── Color Schemes
    ├── Themes
    └── Branding
```

---

## [FUNCIONALIDADES] Funcionalidades Planificadas

### Gráficos de Precios

#### Gráficos de Velas (Candlestick)

Visualización de precios OHLC con estilo profesional:

```python
chart = create_candlestick_chart(
    price_data=price_data,
    title="AAPL - Precios Históricos",
    indicators=['SMA_50', 'SMA_200', 'Bollinger_Bands']
)
```

**Características**:
- Velas verdes/rojas para subidas/bajadas
- Overlay de medias móviles
- Bandas de Bollinger
- Volumen en subplot inferior

#### Gráficos de Línea

Para visualización más simple:

```python
chart = create_line_chart(
    price_data=price_data['Close'],
    title="AAPL - Precio de Cierre",
    indicators=['SMA_50', 'EMA_20']
)
```

#### Gráficos de Volumen

Visualización de volumen de trading:

```python
volume_chart = create_volume_chart(
    volume_data=price_data['Volume'],
    price_data=price_data['Close']
)
```

### Visualización del Score

#### Gráfico de Breakdown

Muestra cómo se compone el score:

```python
score_chart = create_score_breakdown_chart(
    breakdown=score_breakdown,
    title="Breakdown del Score - AAPL"
)
```

**Tipos**:
- **Waterfall Chart**: Muestra contribución de cada componente
- **Stacked Bar Chart**: Comparación de bloques
- **Treemap**: Visualización jerárquica

#### Gráfico Radar

Comparación multidimensional:

```python
radar_chart = create_radar_chart(
    technical_score=0.55,
    fundamental_score=0.70,
    strategies={
        'momentum': 0.75,
        'value': 0.80,
        'quality': 0.70
    }
)
```

#### Gráfico de Comparación

Compara múltiples activos:

```python
comparison_chart = create_comparison_chart(
    symbols=['AAPL', 'MSFT', 'GOOGL'],
    scores=[0.65, 0.55, 0.60]
)
```

### Tablas Ejecutivas

#### Tabla Resumen

Métricas clave en formato tabla:

```python
summary_table = create_summary_table(
    symbol='AAPL',
    current_price=150.0,
    score=0.65,
    classification='Buy',
    key_metrics={
        'PE': 25.5,
        'ROE': 0.15,
        'Debt/Equity': 1.2
    }
)
```

#### Tabla de Comparación

Compara múltiples activos:

```python
comparison_table = create_comparison_table(
    symbols=['AAPL', 'MSFT', 'GOOGL'],
    metrics=['PE', 'ROE', 'Score', 'Classification']
)
```

#### Tabla Histórica

Evolución de métricas en el tiempo:

```python
historical_table = create_historical_table(
    data=historical_data,
    metrics=['Revenue', 'Earnings', 'ROE'],
    years=5
)
```

### Reportes Completos

#### Reporte PDF

Genera reporte completo en PDF:

```python
pdf_report = generate_pdf_report(
    symbol='AAPL',
    decision=decision_result,
    price_chart=price_chart,
    score_chart=score_chart,
    tables=[summary_table, comparison_table],
    output_path='reports/AAPL_report.pdf'
)
```

**Contenido del reporte**:
- Portada con logo y fecha
- Resumen ejecutivo
- Gráficos de precios
- Breakdown del score
- Tablas de métricas
- Recomendaciones
- Apéndices con datos detallados

#### Reporte HTML

Genera reporte interactivo en HTML:

```python
html_report = generate_html_report(
    symbol='AAPL',
    decision=decision_result,
    charts=[price_chart, score_chart],
    tables=[summary_table],
    output_path='reports/AAPL_report.html',
    interactive=True
)
```

**Características**:
- Interactividad con Plotly
- Navegación por secciones
- Exportación a PDF
- Responsive design

#### Dashboard Interactivo

Dashboard completo con múltiples visualizaciones:

```python
dashboard = create_dashboard(
    symbols=['AAPL', 'MSFT', 'GOOGL'],
    data=all_data,
    layout='grid'  # 'grid', 'tabs', 'accordion'
)
```

---

## [USO] Uso Previsto

### Inicialización

```python
from src.final.visualization import VisualizationEngine

# Crear engine de visualización
viz = VisualizationEngine(
    style='professional',  # 'professional', 'minimal', 'colorful'
    theme='light'          # 'light', 'dark'
)
```

### Crear Gráficos Individuales

```python
# Gráfico de precios
price_chart = viz.create_price_chart(
    price_data=price_data,
    symbol='AAPL',
    indicators=['SMA_50', 'RSI']
)

# Gráfico de score
score_chart = viz.create_score_chart(
    breakdown=score_breakdown,
    symbol='AAPL'
)

# Tabla resumen
summary_table = viz.create_summary_table(
    decision=decision_result,
    key_metrics=fundamental_data
)
```

### Generar Reporte Completo

```python
# Generar reporte completo
report = viz.generate_full_report(
    symbol='AAPL',
    price_data=price_data,
    decision=decision_result,
    score_breakdown=score_breakdown,
    fundamental_data=fundamental_data,
    output_format='pdf',  # 'pdf', 'html', 'both'
    output_path='reports/'
)

# Report contiene paths a archivos generados
print(f"PDF: {report['pdf']}")
print(f"HTML: {report['html']}")
```

### Crear Dashboard

```python
# Dashboard interactivo
dashboard = viz.create_dashboard(
    symbols=['AAPL', 'MSFT'],
    data={
        'AAPL': {'price': ..., 'decision': ..., 'score': ...},
        'MSFT': {'price': ..., 'decision': ..., 'score': ...}
    },
    output_path='dashboards/portfolio_dashboard.html'
)
```

---

## [ESTILOS] Estilos y Temas

### Esquemas de Color

#### Profesional (Default)

- Azul corporativo para elementos principales
- Verde/rojo para señales positivas/negativas
- Grises para elementos neutros

#### Minimal

- Escala de grises
- Acento en color para elementos clave
- Diseño limpio y simple

#### Colorful

- Paleta vibrante
- Múltiples colores para diferenciación
- Ideal para presentaciones

### Temas

#### Light Theme (Default)

- Fondo blanco
- Texto oscuro
- Ideal para impresión

#### Dark Theme

- Fondo oscuro
- Texto claro
- Ideal para pantallas

---

## [FORMATOS] Formatos de Salida

### Gráficos

- **PNG**: Alta resolución para documentos
- **SVG**: Vectorial, escalable
- **PDF**: Para reportes
- **HTML**: Interactivo con Plotly

### Tablas

- **HTML**: Para reportes web
- **LaTeX**: Para documentos académicos
- **CSV**: Para exportación de datos
- **Excel**: Para análisis adicional

### Reportes

- **PDF**: Documento completo y portable
- **HTML**: Interactivo y navegable
- **Markdown**: Para documentación

---

## [BIBLIOTECAS] Bibliotecas Utilizadas

### Visualización

- **Matplotlib**: Gráficos estáticos base
- **Plotly**: Gráficos interactivos
- **Seaborn**: Estilos y gráficos estadísticos
- **mplfinance**: Gráficos de velas especializados

### Tablas

- **Pandas**: Manipulación y formato de tablas
- **tabulate**: Formato de tablas en texto

### Reportes

- **ReportLab**: Generación de PDFs
- **Jinja2**: Plantillas para HTML
- **WeasyPrint**: HTML a PDF

---

## [EJEMPLOS] Ejemplos de Visualizaciones

### Gráfico de Precios con Indicadores

```
┌─────────────────────────────────────────┐
│  AAPL - Precios Históricos (1 año)     │
│                                         │
│  $200 ┤                                 │
│       │    ╱╲                           │
│  $180 ┤  ╱  ╲╲                          │
│       │ ╱    ╲╲    ╱╲                  │
│  $160 ┤╱      ╲╲  ╱  ╲                  │
│       └────────┴──┴────┴─────────────   │
│         SMA_50  SMA_200  Precio         │
│                                         │
│  Vol ┤███████████████████████████████  │
│       └───────────────────────────────  │
└─────────────────────────────────────────┘
```

### Gráfico de Score Breakdown

```
Score Total: 0.65 (Buy)
┌─────────────────────────────────────┐
│ Technical (40%)    │███████░░░░│ 55%│
│ Fundamental (60%)  │██████████│ 70%│
│                     └───────────────│
│ Total               │██████████│ 65%│
└─────────────────────────────────────┘
```

### Tabla Resumen

```
┌─────────────────────────────────────────┐
│ AAPL - Apple Inc.                       │
├─────────────────────────────────────────┤
│ Precio Actual:        $150.00           │
│ Score:                0.65 (Buy)       │
│ Confianza:            75%               │
├─────────────────────────────────────────┤
│ PE Ratio:             25.5              │
│ ROE:                  15.0%             │
│ Debt/Equity:          1.2               │
│ Market Cap:           $2.5T             │
└─────────────────────────────────────────┘
```

---

## [INTEGRACION] Integración con Otros Módulos

### Entrada

- **Datos de precios**: Del módulo `data/cleaning`
- **Decision result**: Del módulo `final/decision`
- **Score breakdown**: Del módulo `analisis/scoring`
- **Datos fundamentales**: Del módulo `data/raw`

### Salida

- **Gráficos**: Archivos de imagen o objetos interactivos
- **Tablas**: HTML, LaTeX, o DataFrames
- **Reportes**: Archivos PDF/HTML

### Flujo

```
Price Data + Decision + Score Breakdown
    ↓
VisualizationEngine
    ↓
Charts + Tables + Reports
    ↓
Usuario / Archivos
```

---

## [CONFIGURACION] Configuración Avanzada

### Personalización de Estilos

```python
viz = VisualizationEngine(
    colors={
        'positive': '#00FF00',
        'negative': '#FF0000',
        'neutral': '#808080'
    },
    font_family='Arial',
    font_size=12
)
```

### Configuración de Reportes

```python
report_config = {
    'include_charts': True,
    'include_tables': True,
    'include_appendix': True,
    'page_size': 'A4',
    'orientation': 'portrait'
}

report = viz.generate_report(
    data=data,
    config=report_config
)
```

---

## [VALIDACION] Validación y Testing

### Validación de Gráficos

- Verificación de datos de entrada
- Validación de formatos de salida
- Testing de estilos y temas

### Validación de Reportes

- Verificación de contenido completo
- Validación de formato PDF/HTML
- Testing de navegación y enlaces

---

## [LIMITACIONES] Limitaciones Conocidas

- **Rendimiento**: Reportes grandes pueden ser lentos
- **Dependencias**: Requiere múltiples bibliotecas
- **Personalización limitada**: Estilos predefinidos
- **No interactivo en PDF**: Solo HTML es interactivo

---

## [FUTURO] Mejoras Futuras

- **Dashboards en tiempo real**: Actualización automática
- **Exportación a Excel**: Reportes en formato Excel
- **Templates personalizables**: Plantillas configurables
- **Integración con web**: Servidor web para dashboards
- **Animaciones**: Gráficos animados para presentaciones
- **Exportación a PowerPoint**: Generación de presentaciones
- **Multi-idioma**: Soporte para múltiples idiomas
- **Accesibilidad**: Mejoras para usuarios con discapacidades
