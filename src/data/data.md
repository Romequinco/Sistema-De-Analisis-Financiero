# [DATA] Módulo de Datos Financieros

## [OBJETIVO] Objetivo

Este módulo se encarga de **obtener y preparar** datos financieros para su uso en el sistema de análisis.

El módulo `data` es la primera etapa del pipeline y proporciona datos limpios y normalizados a los módulos de análisis.

## [ESTRUCTURA] Estructura del Módulo

```
src/data/
├── raw/          Extracción de datos desde fuentes externas
│   └── data.md   Documentación exhaustiva del módulo raw
└── cleaning/     Limpieza y preprocesamiento de datos
    └── cleaning.md   Documentación exhaustiva del módulo cleaning
```

## [COMPONENTES] Componentes

### Raw (`src/data/raw/`)

Módulo de extracción de datos desde Yahoo Finance.

**Características principales**:
- Extracción de datos desde Yahoo Finance usando yfinance
- Cache local con TTL configurable (1 hora por defecto)
- Reintentos automáticos con backoff exponencial
- Manejo robusto de errores y fallback a cache
- Soporte para múltiples tipos de datos (precios, fundamentales, estados financieros)

**Ver documentación completa**: `src/data/raw/data.md`

### Cleaning (`src/data/cleaning/`)

Módulo de limpieza y preprocesamiento de datos financieros.

**Características principales**:
- Limpieza y normalización de datos OHLCV
- Validación de relaciones OHLC (High >= Low, etc.)
- Manejo inteligente de valores nulos (forward-fill, backward-fill, interpolate)
- Eliminación de duplicados y detección de outliers
- Añadir columnas auxiliares (returns, log_returns, volatilidad)
- Metadata completa de todas las transformaciones

**Ver documentación completa**: `src/data/cleaning/cleaning.md`

## [USO] Uso Básico

```python
from src.data import DataProvider, DataCleaner

# Extraer datos
provider = DataProvider()
raw_data = provider.get_price_data("AAPL", period="1y", interval="1d")

# Limpiar datos
cleaner = DataCleaner()
cleaned_data, metadata = cleaner.clean_price_data(raw_data, symbol="AAPL")

# Ver qué se limpió
print(metadata.summary())
```

## [FLUJO] Flujo de Datos

```
DataProvider (raw)
    ↓
Datos Crudos
    ↓
DataCleaner (cleaning)
    ↓
Datos Limpios
    ↓
Módulos de Análisis
```

## [ESTADO] Estado

- ✅ [IMPLEMENTADO] Extracción desde Yahoo Finance (`raw/`)
- ✅ [IMPLEMENTADO] Limpieza y preprocesamiento (`cleaning/`)

## [DOCUMENTACION] Documentación Detallada

Para información exhaustiva sobre cada componente:

- **Extracción de datos**: Ver `src/data/raw/data.md`
- **Limpieza de datos**: Ver `src/data/cleaning/cleaning.md`
