# src/capital_gains_calculator/application/use_cases/__init__.py

# Exposes use case classes so they can be imported from the package
from .calculate_taxes_from_operations import \
    CalculateTaxesFromOperationsUseCase

__all__ = ["CalculateTaxesFromOperationsUseCase"]
