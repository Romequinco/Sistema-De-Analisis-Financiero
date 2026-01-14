# [DATA] Módulo de Extracción de Datos

## [OBJETIVO] Objetivo

Este módulo proporciona una interfaz unificada para obtener datos financieros de múltiples fuentes, principalmente usando **yfinance** como proveedor principal.

## [CARACTERISTICAS] Características Principales

- **Abstracción de fuente de datos**: Interfaz única independiente del proveedor
- **Cache local**: Evita llamadas innecesarias a APIs externas
- **Manejo robusto de errores**: Gestión adecuada de fallos y datos faltantes
- **Normalización**: Datos consistentes independientemente de la fuente
- **Múltiples tipos de datos**: Precios, fundamentales, estados financieros

## [ARQUITECTURA] Arquitectura

```
DataProvider
├── Cache Management
│   ├── Validación TTL
│   ├── Guardado/Lectura
│   └── Limpieza
├── Price Data
│   └── Históricos OHLCV
├── Fundamental Data
│   └── Métricas y ratios
└── Financial Statements
    ├── Income Statement
    ├── Balance Sheet
    └── Cash Flow
```

## [USO] Uso Básico

### Inicialización

```python
from src.data import DataProvider

# Con parámetros por defecto
provider = DataProvider()

# Con configuración personalizada
provider = DataProvider(
    cache_dir="data/raw",
    timeout=120,      # Timeout en segundos
    max_retries=5    # Número de reintentos
)
```

### Obtener datos de precios

```python
# Datos históricos de 1 año
price_data = provider.get_price_data("AAPL", period="1y", interval="1d")

# Columnas disponibles:
# - Open, High, Low, Close
# - Volume
# - Dividends
# - Stock Splits
```

### Obtener datos fundamentales

```python
fundamental = provider.get_fundamental_data("AAPL")

# Incluye:
# - Ratios de valoración (PE, PB, PS)
# - Métricas de crecimiento
# - Ratios de rentabilidad (ROE, ROA)
# - Ratios de solvencia
# - Información de mercado
```

### Obtener estados financieros

```python
# Estado de resultados
income = provider.get_financial_statements("AAPL", "income")

# Balance general
balance = provider.get_financial_statements("AAPL", "balance")

# Flujo de efectivo
cashflow = provider.get_financial_statements("AAPL", "cashflow")
```

### Obtener todos los datos

```python
all_data = provider.get_all_data("AAPL", period="1y")

# Retorna diccionario con:
# - price_data
# - fundamental_data
# - income_statement
# - balance_sheet
# - cashflow_statement
```

### Función de conveniencia

```python
from src.data import get_data

data = get_data("AAPL", period="1y")
```

## [VISUALIZACION] Funciones de Visualización

El módulo incluye funciones auxiliares para crear tablas formateadas:

### Crear tablas de datos fundamentales

```python
from src.data import create_fundamental_tables

fundamental = provider.get_fundamental_data("AAPL")
tables = create_fundamental_tables(fundamental)

# Retorna diccionario con DataFrames organizados:
# - tables['general']: Información general
# - tables['valuation']: Métricas de valoración
# - tables['profitability']: Métricas de rentabilidad
# - tables['growth']: Métricas de crecimiento
# - tables['health']: Salud financiera
# - tables['prices']: Precios y recomendaciones
```

### Crear tablas históricas

```python
from src.data import create_historical_tables

income = provider.get_financial_statements("AAPL", "income")
balance = provider.get_financial_statements("AAPL", "balance")
cashflow = provider.get_financial_statements("AAPL", "cashflow")

historical_tables = create_historical_tables(
    income, balance, cashflow, max_years=5
)

# Retorna diccionario con:
# - historical_tables['income_history']: Evolución de ingresos
# - historical_tables['balance_history']: Evolución del balance
# - historical_tables['cashflow_history']: Evolución del flujo de efectivo
# - historical_tables['ratios_history']: Evolución de ratios clave
```

### Formatear números

```python
from src.data import format_number

format_number(1500000000)  # "$1.50B"
format_number(50000000)    # "$50.00M"
format_number(1000)        # "$1.00K"
```

## [CACHE] Sistema de Cache

El módulo implementa un sistema de cache local para:

- Reducir llamadas a APIs externas
- Mejorar velocidad de respuesta
- Trabajar offline con datos recientes

**TTL por defecto**: 1 hora

**Ubicación**: `data/raw/`

**Formato**: Archivos pickle (.pkl)

### Limpiar cache

```python
# Limpiar todo el cache
provider.clear_cache()

# Limpiar cache de un símbolo específico
provider.clear_cache("AAPL")
```

## [PERIODOS] Períodos Disponibles

Para datos de precios:

- `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

## [INTERVALOS] Intervalos Disponibles

- `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

## [TIPOS_ACTIVOS] Tipos de Activos Soportados

- Acciones (ej: "AAPL", "MSFT")
- ETFs (ej: "SPY", "QQQ")
- Criptomonedas (ej: "BTC-USD", "ETH-USD")
- Índices (ej: "^GSPC")
- Cualquier símbolo soportado por Yahoo Finance

## [ERRORES] Manejo de Errores

El módulo maneja automáticamente:

- Símbolos inválidos
- Datos faltantes
- Errores de red y timeouts
- Problemas de cache
- Reintentos automáticos con backoff exponencial
- Uso de cache antiguo cuando falla la descarga

**Características de robustez:**
- Reintentos automáticos (3 por defecto, configurable)
- Timeout configurable (60 segundos por defecto)
- Backoff exponencial entre reintentos
- Fallback a cache antiguo si la descarga falla
- Manejo robusto de valores None y datos faltantes

Todos los errores se registran en el logger y se propagan con mensajes descriptivos.

## [FUTURO] Mejoras Futuras

- Soporte para múltiples proveedores (Alpha Vantage, Polygon, etc.)
- Cache distribuido (Redis)
- Validación de datos
- Transformaciones automáticas
- Soporte para datos en tiempo real
