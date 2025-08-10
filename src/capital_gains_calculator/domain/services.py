# src/capital_gains_calculator/domain/services.py
from decimal import Decimal
from typing import Callable, Dict, List

from .models import Operation, TaxResult

TAX_EXEMPTION_LIMIT = Decimal("20000.00")
TAX_RATE = Decimal("0.20")


class TaxCalculatorService:
    def __init__(self):
        self.total_shares = 0
        self.weighted_average_cost = Decimal("0.00")
        self.accumulated_loss = Decimal("0.00")

        self._handlers: Dict[str, Callable[[Operation], TaxResult]] = {
            "buy": self._handle_buy,
            "sell": self._handle_sell,
        }

    def _update_weighted_average_cost(self, bought_shares: int, buy_price: Decimal):
        current_total_cost = self.total_shares * self.weighted_average_cost
        new_total_cost = bought_shares * buy_price
        self.total_shares += bought_shares
        if self.total_shares > 0:
            self.weighted_average_cost = (
                current_total_cost + new_total_cost
            ) / self.total_shares

    def _handle_buy(self, op: Operation) -> TaxResult:
        """Handles the logic for a buy operation."""
        self._update_weighted_average_cost(op.quantity, op.unit_cost)
        return TaxResult(tax=Decimal("0.00"))

    def _process_loss(self, loss: Decimal) -> TaxResult:
        """Processes a loss, adding it to the accumulated total."""
        self.accumulated_loss += abs(loss)
        return TaxResult(tax=Decimal("0.00"))

    def _process_profit(self, profit: Decimal, op: Operation) -> TaxResult:
        """Processes a profit, considering tax exemption and accumulated losses."""
        total_value = op.unit_cost * op.quantity
        if total_value <= TAX_EXEMPTION_LIMIT:
            return TaxResult(tax=Decimal("0.00"))

        taxable_profit = profit - self.accumulated_loss
        if taxable_profit <= 0:
            self.accumulated_loss -= profit
            return TaxResult(tax=Decimal("0.00"))

        tax = taxable_profit * TAX_RATE
        self.accumulated_loss = Decimal("0.00")
        return TaxResult(tax=tax)

    def _handle_sell(self, op: Operation) -> TaxResult:
        """Handles a sell operation, delegating to the profit/loss methods."""
        profit_or_loss = (op.unit_cost - self.weighted_average_cost) * op.quantity
        self.total_shares -= op.quantity

        if profit_or_loss < 0:
            return self._process_loss(profit_or_loss)
        else:
            return self._process_profit(profit_or_loss, op)

    def process(self, operations: List[Operation]) -> List[TaxResult]:
        """Processes a list of operations using the dispatcher to call the correct handler."""
        results = []
        for op in operations:
            handler = self._handlers.get(op.operation)
            if handler:
                tax_result = handler(op)
                results.append(tax_result)
        return results
