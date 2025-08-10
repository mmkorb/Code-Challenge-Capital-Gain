# src/capital_gains_calculator/domain/models.py
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Operation:
    """Represents a single buy or sell stock operation in the domain."""

    operation: str
    unit_cost: Decimal
    quantity: int


@dataclass(frozen=True)
class TaxResult:
    """Represents the tax calculation result for an operation in the domain."""

    tax: Decimal
