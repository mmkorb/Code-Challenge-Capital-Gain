from typing import List

from ...domain.models import Operation
from ...domain.services import TaxCalculatorService
from ..dtos import OperationDTO, TaxResultDTO


class CalculateTaxesFromOperationsUseCase:
    def __init__(self, tax_calculator: TaxCalculatorService):
        # Receives the domain service as a dependency
        self.tax_calculator = tax_calculator

    def execute(self, operations_dto: List[OperationDTO]) -> List[TaxResultDTO]:
        """
        Orchestrates data conversion and calls the domain service.
        """
        # 1. Converts application DTOs to domain Models
        operations_domain = [
            Operation(op.operation, op.unit_cost, op.quantity) for op in operations_dto
        ]

        # 2. Calls the domain service for the ACTUAL business logic
        tax_results_domain = self.tax_calculator.process(operations_domain)

        # 3. Converts domain results back to DTOs
        tax_results_dto = [TaxResultDTO(tax=res.tax) for res in tax_results_domain]
        return tax_results_dto
