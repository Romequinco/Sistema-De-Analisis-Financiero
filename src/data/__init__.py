"""
Módulo de datos financieros.

Incluye:
- raw: Extracción de datos desde Yahoo Finance
- cleaning: Limpieza y preprocesamiento de datos
"""

# Re-exportar desde raw para compatibilidad
from .raw import (
    DataProvider,
    get_data,
    format_number,
    create_fundamental_tables,
    create_historical_tables
)

# Exportar cleaning
from .cleaning import (
    DataCleaner,
    CleaningMetadata,
    clean_price_data,
    clean_fundamental_data,
    clean_financial_statement
)

__all__ = [
    # Raw data
    "DataProvider",
    "get_data",
    "format_number",
    "create_fundamental_tables",
    "create_historical_tables",
    # Cleaning
    "DataCleaner",
    "CleaningMetadata",
    "clean_price_data",
    "clean_fundamental_data",
    "clean_financial_statement"
]
