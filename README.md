# 📊 Proyecto de Evaluación de Activos Financieros

## 🎯 Objetivo
Este proyecto tiene como objetivo evaluar activos financieros (acciones, ETFs, criptomonedas, etc.) de forma **agnóstica al mercado**, combinando **análisis técnico** y **análisis fundamental** en un sistema cuantitativo, explicable y modular.

El resultado final es un **score numérico**, una **clasificación discreta** (Strong Buy / Buy / Neutral / Sell / Strong Sell) y una **explicación detallada** del porqué de la decisión.

El proyecto está diseñado para:
- Uso experimental pero cercano a producción
- Apoyo personal a decisiones de inversión
- Aprendizaje profundo y portfolio profesional

---

## 🧠 Filosofía del sistema

- Modular y extensible
- Explicable (no caja negra)
- Preparado para crecer (backtesting, ML, brokers)
- Visual y didáctico (notebooks)
- Separación clara entre datos, análisis, scoring y decisión

---

## 🧱 Arquitectura General

El sistema sigue un pipeline claro:

1. Extracción de datos
2. Análisis técnico
3. Análisis fundamental
4. Sistema de scoring
5. Motor de decisión
6. Visualización y reporting

Cada paso es independiente, testeable y reemplazable.

---

## 📂 Estructura del repositorio

```
project/
│
├── src/
│   ├── data/
│   ├── technical/
│   ├── fundamental/
│   ├── scoring/
│   ├── decision/
│   ├── visualization/
│   ├── config/
│   └── utils/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── docs/
│
├── tests/
│
├── .github/workflows/
│
└── README.md
```

---

## 📦 Estructura interna de cada módulo

Cada módulo contiene obligatoriamente:

- `module.py` → lógica principal
- `module.md` → explicación visual y conceptual
- `module_test.ipynb` → notebook de test con:
  - prints intermedios
  - tablas
  - visualizaciones
  - debugging

---

## 📊 Resultados esperados

- Score numérico total
- Clasificación discreta
- Breakdown del score
- Tablas ejecutivas
- Gráficos interactivos
- Explicación textual legible

---

## 🔮 Futuro del proyecto

Arquitectura preparada para:
- Backtesting
- Optimización de parámetros
- Machine Learning
- Conexión con brokers reales
- Nuevas estrategias y mercados

---

⚠️ **Disclaimer**: Este proyecto no constituye asesoramiento financiero.
