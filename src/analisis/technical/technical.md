# [TECHNICAL] Módulo de Análisis Técnico

## [UBICACION] Ubicación

`src/analisis/technical/`

## [OBJETIVO] Objetivo

Este módulo implementa **indicadores técnicos** y **estrategias de trading** basadas en análisis técnico para generar señales normalizadas que alimentan el sistema de scoring.

---

## [ESTADO] Estado Actual

Módulo en desarrollo inicial. Pendiente de implementación.

---

## [ARQUITECTURA] Arquitectura del Módulo

```
TechnicalAnalyzer
├── Indicadores de Tendencia
│   ├── SMA (Simple Moving Average)
│   ├── EMA (Exponential Moving Average)
│   ├── WMA (Weighted Moving Average)
│   └── MACD (Moving Average Convergence Divergence)
├── Indicadores de Momentum
│   ├── RSI (Relative Strength Index)
│   ├── Stochastic Oscillator
│   ├── Williams %R
│   └── CCI (Commodity Channel Index)
├── Indicadores de Volatilidad
│   ├── Bollinger Bands
│   ├── ATR (Average True Range)
│   └── Keltner Channels
├── Indicadores de Volumen
│   ├── OBV (On-Balance Volume)
│   ├── Volume SMA
│   └── Volume Profile
└── Estrategias Técnicas
    ├── Momentum Strategy
    ├── Mean Reversion Strategy
    ├── Breakout Strategy
    └── Trend Following Strategy
```

---

## [FUNCIONALIDADES] Funcionalidades Planificadas

### Indicadores Técnicos Básicos

#### Medias Móviles

- **SMA (Simple Moving Average)**: Media aritmética simple
- **EMA (Exponential Moving Average)**: Media exponencial ponderada
- **WMA (Weighted Moving Average)**: Media ponderada linealmente
- **Uso**: Identificar tendencias y cruces de medias

#### Indicadores de Momentum

- **RSI (Relative Strength Index)**: Fuerza relativa (0-100)
  - RSI > 70: Sobrecompra
  - RSI < 30: Sobreventa
- **Stochastic Oscillator**: Posición relativa en rango
- **Williams %R**: Momentum inverso
- **CCI (Commodity Channel Index)**: Desviación de la media

#### Indicadores de Volatilidad

- **Bollinger Bands**: Bandas de volatilidad alrededor de SMA
  - Precio cerca de banda superior: Posible sobrecompra
  - Precio cerca de banda inferior: Posible sobreventa
- **ATR (Average True Range)**: Volatilidad absoluta
- **Keltner Channels**: Bandas basadas en ATR

#### Indicadores de Volumen

- **OBV (On-Balance Volume)**: Acumulación de volumen
- **Volume SMA**: Media móvil de volumen
- **Volume Profile**: Distribución de volumen por precio

### Estrategias Técnicas

#### Momentum Strategy

- Identifica activos con momentum positivo/negativo
- Señales basadas en múltiples indicadores de momentum
- Normalización: -1 (momentum negativo fuerte) a +1 (momentum positivo fuerte)

#### Mean Reversion Strategy

- Identifica activos que se desvían de su media
- Señales basadas en Bollinger Bands, RSI extremos
- Normalización: -1 (sobrecompra extrema) a +1 (sobreventa extrema)

#### Breakout Strategy

- Identifica rupturas de niveles de soporte/resistencia
- Señales basadas en volumen y volatilidad
- Normalización: -1 (ruptura bajista) a +1 (ruptura alcista)

#### Trend Following Strategy

- Identifica y sigue tendencias establecidas
- Señales basadas en cruces de medias y MACD
- Normalización: -1 (tendencia bajista) a +1 (tendencia alcista)

---

## [USO] Uso Previsto

### Inicialización

```python
from src.analisis.technical import TechnicalAnalyzer

# Crear analizador técnico
analyzer = TechnicalAnalyzer(
    price_data=cleaned_price_data,
    volume_data=cleaned_price_data['Volume']
)
```

### Calcular Indicadores

```python
# Calcular RSI
rsi = analyzer.calculate_rsi(period=14)

# Calcular MACD
macd, signal, histogram = analyzer.calculate_macd()

# Calcular Bollinger Bands
upper, middle, lower = analyzer.calculate_bollinger_bands(period=20, std=2)
```

### Generar Señales de Estrategias

```python
# Señal de momentum
momentum_signal = analyzer.momentum_strategy()

# Señal de mean reversion
mean_reversion_signal = analyzer.mean_reversion_strategy()

# Señal de breakout
breakout_signal = analyzer.breakout_strategy()

# Señal de trend following
trend_signal = analyzer.trend_following_strategy()
```

### Obtener Señales Normalizadas

```python
# Todas las señales normalizadas (-1 a +1)
signals = analyzer.get_all_signals()

# Retorna diccionario:
# {
#     'momentum': 0.75,
#     'mean_reversion': -0.30,
#     'breakout': 0.50,
#     'trend_following': 0.60
# }
```

---

## [NORMALIZACION] Normalización de Señales

Todas las señales se normalizan al rango **[-1, +1]**:

- **+1**: Señal muy alcista (compra fuerte)
- **0**: Neutral
- **-1**: Señal muy bajista (venta fuerte)

### Ventajas de la Normalización

- Comparabilidad entre estrategias diferentes
- Agregación sencilla en el módulo de scoring
- Interpretación intuitiva
- Escalabilidad a nuevas estrategias

---

## [INTEGRACION] Integración con Otros Módulos

### Entrada

- **Datos limpios**: Precios OHLCV del módulo `data/cleaning`
- **Requisitos**:
  - Datos ordenados cronológicamente
  - Sin gaps temporales significativos
  - Returns calculados

### Salida

- **Señales normalizadas**: Diccionario con señales de cada estrategia
- **Formato**: `{'strategy_name': signal_value}` donde `signal_value` ∈ [-1, +1]

### Flujo

```
Datos Limpios (OHLCV)
    ↓
TechnicalAnalyzer
    ↓
Señales Normalizadas
    ↓
Scoring Engine
```

---

## [ALGORITMOS] Algoritmos Clave

### RSI (Relative Strength Index)

```
RSI = 100 - (100 / (1 + RS))
RS = Average Gain / Average Loss
```

- Período típico: 14 días
- RSI > 70: Sobrecompra (señal bajista)
- RSI < 30: Sobreventa (señal alcista)

### MACD (Moving Average Convergence Divergence)

```
MACD Line = EMA(12) - EMA(26)
Signal Line = EMA(9) of MACD Line
Histogram = MACD Line - Signal Line
```

- Cruce alcista: MACD cruza por encima de Signal
- Cruce bajista: MACD cruza por debajo de Signal

### Bollinger Bands

```
Middle Band = SMA(20)
Upper Band = Middle + (2 * StdDev)
Lower Band = Middle - (2 * StdDev)
```

- Precio toca banda superior: Posible sobrecompra
- Precio toca banda inferior: Posible sobreventa

---

## [CONFIGURACION] Parámetros Configurables

### Períodos por Defecto

- **RSI**: 14 períodos
- **MACD**: 12, 26, 9 períodos
- **Bollinger Bands**: 20 períodos, 2 desviaciones estándar
- **SMA/EMA**: 50, 200 períodos (comúnmente usados)

### Personalización

```python
analyzer = TechnicalAnalyzer(
    rsi_period=14,
    macd_fast=12,
    macd_slow=26,
    macd_signal=9,
    bollinger_period=20,
    bollinger_std=2
)
```

---

## [VALIDACION] Validación y Testing

### Validación de Indicadores

- Comparación con implementaciones estándar (pandas_ta, ta-lib)
- Verificación de rangos (RSI entre 0-100, señales entre -1 y +1)
- Testing con datos históricos conocidos

### Backtesting

- Las señales deben ser históricamente válidas (no usar datos futuros)
- Validación de que las señales se generan correctamente en el tiempo
- Verificación de que no hay look-ahead bias

---

## [LIMITACIONES] Limitaciones Conocidas

- Los indicadores técnicos son **lagging** (retrasados)
- Pueden generar **señales falsas** en mercados laterales
- Requieren **datos suficientes** (mínimo de períodos históricos)
- No consideran **eventos fundamentales** (solo precio y volumen)

---

## [FUTURO] Mejoras Futuras

- Indicadores avanzados (Ichimoku, Fibonacci)
- Machine learning para optimización de parámetros
- Análisis multi-timeframe
- Detección automática de patrones (candlestick patterns)
- Integración con datos de sentimiento
- Optimización de estrategias con walk-forward analysis
