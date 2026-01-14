# Indicadores Técnicos Compuestos

## [OBJETIVO] Objetivo

Este módulo contiene **indicadores compuestos avanzados** que combinan múltiples componentes o conceptos para proporcionar análisis más completo y sofisticado.

A diferencia de los indicadores básicos que miden un aspecto específico (tendencia, momentum, volatilidad), los indicadores compuestos integran múltiples elementos para ofrecer una visión más holística del mercado.

---

## [DIFERENCIA] Diferencia con Indicadores Básicos

### Indicadores Básicos
- Miden un aspecto específico (ej: RSI mide momentum)
- Cálculo directo y simple
- Interpretación más directa
- Ejemplos: SMA, RSI, ATR

### Indicadores Compuestos
- Combinan múltiples componentes
- Cálculo más complejo
- Interpretación más rica pero también más compleja
- Ejemplos: MACD, Ichimoku, SuperTrend

---

## [MACD] MACD (Moving Average Convergence Divergence)

### Qué es

El MACD combina tres componentes:
1. **MACD Line**: Diferencia entre EMA rápida (12) y EMA lenta (26)
2. **Signal Line**: EMA del MACD Line (9 períodos)
3. **Histogram**: Diferencia entre MACD Line y Signal Line

### Qué problema resuelve

- Identifica cambios en momentum
- Detecta cambios de tendencia
- Proporciona señales de compra/venta
- Identifica divergencias con precio

### Cuándo usarlo

- Confirmar cambios de tendencia
- Identificar momentum alcista/bajista
- Detectar divergencias (señal de reversión)
- Combinar con otros indicadores para confirmación

### Ventajas

- Ampliamente reconocido y utilizado
- Proporciona múltiples señales (cruces, divergencias)
- Funciona en múltiples timeframes
- Histogram muestra fuerza del momentum

### Limitaciones

- Puede generar señales falsas en mercados laterales
- Requiere interpretación de múltiples componentes
- Puede tener retraso en cambios de tendencia
- Mejor en mercados con tendencia

### Interpretación clásica

**Cruces**:
- MACD cruza por encima de Signal: Señal alcista (compra)
- MACD cruza por debajo de Signal: Señal bajista (venta)

**Histogram**:
- Histogram positivo y creciente: Momentum alcista fuerte
- Histogram negativo y decreciente: Momentum bajista fuerte
- Histogram cerca de cero: Momentum débil

**Divergencias**:
- Precio hace nuevo máximo pero MACD no: Divergencia bajista (posible reversión)
- Precio hace nuevo mínimo pero MACD no: Divergencia alcista (posible reversión)

**Ejemplo conceptual**:
Si el precio sube de $100 a $120 y el MACD Line sube de 0.5 a 2.0 mientras el Signal sube de 0.3 a 1.5, el Histogram aumenta de 0.2 a 0.5, indicando momentum alcista fuerte y creciente.

---

## [ICHIMOKU] Ichimoku Cloud (Nube de Ichimoku)

### Qué es

Sistema completo de análisis técnico japonés con 5 componentes:
1. **Tenkan-sen**: Línea de conversión (9 períodos)
2. **Kijun-sen**: Línea base (26 períodos)
3. **Senkou Span A**: Línea líder A (promedio de Tenkan y Kijun, desplazada 26 períodos adelante)
4. **Senkou Span B**: Línea líder B (52 períodos, desplazada 26 períodos adelante)
5. **Chikou Span**: Línea retrasada (precio de cierre desplazado 26 períodos atrás)

La **nube (Kumo)** es el área entre Senkou Span A y Senkou Span B.

### Qué problema resuelve

- Proporciona visión completa del mercado en un solo indicador
- Identifica tendencias, soportes/resistencias y momentum
- Proporciona señales de entrada y salida
- Muestra estructura de mercado completa

### Cuándo usarlo

- Análisis completo de mercado en un solo indicador
- Identificar tendencias fuertes
- Encontrar niveles de soporte/resistencia
- Trading de tendencia

### Ventajas

- Sistema completo (no necesita otros indicadores)
- Proporciona múltiples señales simultáneamente
- La nube actúa como soporte/resistencia dinámico
- Funciona en múltiples timeframes

### Limitaciones

- Complejo de interpretar inicialmente
- Requiere entender todos los componentes
- Puede generar señales contradictorias
- Mejor en mercados con tendencia

### Interpretación clásica

**Posición del precio**:
- Precio por encima de la nube: Tendencia alcista fuerte
- Precio por debajo de la nube: Tendencia bajista fuerte
- Precio dentro de la nube: Tendencia neutral/indecisa

**Nube (Kumo)**:
- Nube verde (Span A > Span B): Momentum alcista
- Nube roja (Span A < Span B): Momentum bajista
- Nube gruesa: Soporte/resistencia fuerte
- Nube delgada: Soporte/resistencia débil

**Cruces**:
- Tenkan cruza por encima de Kijun: Señal alcista
- Tenkan cruza por debajo de Kijun: Señal bajista
- Precio cruza la nube: Posible cambio de tendencia

**Ejemplo conceptual**:
Si el precio está en $100, la nube está entre $95-$105 (verde), Tenkan está en $98 y Kijun está en $96, indica tendencia alcista con momentum positivo. Si el precio cruza por debajo de la nube a $94, sugiere posible cambio a tendencia bajista.

---

## [SUPERTREND] SuperTrend

### Qué es

Indicador de tendencia adaptativo que usa ATR para ajustarse a la volatilidad del mercado. Proporciona una línea que cambia de color según la tendencia.

### Qué problema resuelve

- Identifica tendencias de forma clara y visual
- Se adapta automáticamente a cambios en volatilidad
- Proporciona stops dinámicos
- Señales claras de cambio de tendencia

### Cuándo usarlo

- Trading de tendencia
- Identificar cambios de tendencia
- Como stop dinámico
- En mercados con tendencia clara

### Ventajas

- Señales muy claras (verde/rojo)
- Adaptativo a volatilidad
- Stop dinámico automático
- Fácil de interpretar

### Limitaciones

- No funciona bien en mercados laterales
- Puede generar señales falsas en volatilidad extrema
- Requiere tendencia clara
- Puede tener retraso en cambios de tendencia

### Interpretación clásica

**Color de la línea**:
- SuperTrend verde (por debajo del precio): Tendencia alcista (mantener posición larga)
- SuperTrend rojo (por encima del precio): Tendencia bajista (mantener posición corta)

**Cambio de color**:
- Cambio de verde a rojo: Posible cambio a tendencia bajista (señal de venta)
- Cambio de rojo a verde: Posible cambio a tendencia alcista (señal de compra)

**Ejemplo conceptual**:
Si el precio está en $100 y el SuperTrend está en $95 (verde), indica tendencia alcista. Si el precio baja a $94 y el SuperTrend cruza por encima a $96 (rojo), indica cambio a tendencia bajista.

---

## [ADAPTIVE_MA] Adaptive Moving Average

### Qué es

Media móvil que ajusta su velocidad según las condiciones del mercado (volatilidad). Cuando la volatilidad es alta, la media se vuelve más rápida. Cuando es baja, se vuelve más lenta.

### Qué problema resuelve

- Adapta la velocidad de la media según condiciones de mercado
- Más rápida en alta volatilidad (captura movimientos)
- Más lenta en baja volatilidad (reduce ruido)
- Optimiza el balance entre sensibilidad y suavizado

### Cuándo usarlo

- Cuando se necesita adaptabilidad a condiciones de mercado
- En mercados con volatilidad variable
- Para optimizar balance sensibilidad/suavizado
- Como alternativa a EMAs fijas

### Ventajas

- Se adapta automáticamente a condiciones de mercado
- Balance dinámico entre sensibilidad y suavizado
- Útil en diferentes regímenes de mercado
- Reduce necesidad de ajustar parámetros manualmente

### Limitaciones

- Más compleja que EMAs estándar
- Puede ser difícil de interpretar
- Requiere validación con datos históricos
- Implementación puede variar

### Interpretación clásica

- Similar a EMA pero con velocidad adaptativa
- En alta volatilidad: Se comporta como EMA rápida
- En baja volatilidad: Se comporta como EMA lenta
- Útil como referencia de tendencia adaptativa

**Ejemplo conceptual**:
Si el ATR aumenta de $1 a $3 (alta volatilidad), la Adaptive MA se vuelve más rápida (período efectivo más corto), reaccionando más rápido a cambios. Si el ATR disminuye a $0.5 (baja volatilidad), la Adaptive MA se vuelve más lenta (período efectivo más largo), suavizando más el ruido.

---

## [USO] Uso General

```python
from src.analisis.technical.composite_indicators import macd, ichimoku, supertrend, adaptive_ma

# Calcular indicadores compuestos
df = macd.calculate_macd(df)
df = ichimoku.calculate_ichimoku(df)
df = supertrend.calculate_supertrend(df)
df = adaptive_ma.calculate_adaptive_ma(df)

# Acceder a resultados
df['MACD_Line']  # Línea MACD
df['MACD_Signal']  # Línea de señal
df['MACD_Histogram']  # Histograma

df['Ichimoku_Tenkan']  # Tenkan-sen
df['Ichimoku_Senkou_A']  # Senkou Span A
df['Ichimoku_Cloud_Top']  # Parte superior de la nube
```

---

## [COMBINACION] Combinación con Indicadores Básicos

Los indicadores compuestos funcionan mejor cuando se combinan con indicadores básicos:

**Ejemplo de combinación**:
- MACD + RSI: Confirmar señales de momentum
- Ichimoku + Volume: Confirmar tendencias con volumen
- SuperTrend + ATR: Ajustar parámetros según volatilidad
- Adaptive MA + Bollinger Bands: Combinar tendencia adaptativa con volatilidad

---

## [NOTAS] Notas Importantes

1. **Complejidad**: Los indicadores compuestos son más complejos pero proporcionan análisis más rico.

2. **Interpretación**: Requieren entender todos los componentes para interpretación correcta.

3. **Señales múltiples**: Proporcionan múltiples señales simultáneamente (ventaja y desafío).

4. **Mejor en tendencias**: La mayoría funcionan mejor en mercados con tendencia clara.

5. **Validación**: Siempre validar con datos históricos antes de usar en trading real.
