# src/capital_gains_calculator/infrastructure/di_container.py
from dependency_injector import containers, providers

from ..application.use_cases import CalculateTaxesFromOperationsUseCase
from ..domain.services import TaxCalculatorService


class AppContainer(containers.DeclarativeContainer):
    """DI Container for the Application."""

    # Domain layer
    tax_calculator_service = providers.Factory(  # <-- Defines the service provider
        TaxCalculatorService
    )

    # Application layer
    calculate_taxes_use_case = providers.Factory(
        CalculateTaxesFromOperationsUseCase,
        tax_calculator=tax_calculator_service,  # <-- Injects the service into the use case
    )
