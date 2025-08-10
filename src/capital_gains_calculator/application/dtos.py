# src/capital_gains_calculator/application/dtos.py
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class OperationDTO:
    """DTO for a single operation coming from the infrastructure layer."""

    operation: str
    unit_cost: Decimal
    quantity: int


@dataclass(frozen=True)
class TaxResultDTO:
    """DTO for a single tax result to be sent to the infrastructure layer."""

    tax: Decimal
