# src/capital_gains_calculator/infrastructure/cli/main.py
import json
import sys
from decimal import Decimal
from typing import Any, Dict, List

import typer
from dependency_injector.wiring import inject, Provide

from ..di_container import AppContainer
from ...application.dtos import OperationDTO
from ...application.use_cases import CalculateTaxesFromOperationsUseCase

app = typer.Typer(invoke_without_command=True)


@app.command()
def main():
    """
    Processes capital gains operations from standard input (stdin).
    """
    _execute_process()


@inject
def _execute_process(
    use_case: CalculateTaxesFromOperationsUseCase = Provide[
        AppContainer.calculate_taxes_use_case
    ],
):
    """Contains the actual logic and receives the injected dependency."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break

        operations_dto = _parse_line(line)
        tax_results_dto = use_case.execute(operations_dto)

        output_data = [{"tax": float(result.tax)} for result in tax_results_dto]
        json_output = _format_output(output_data)
        print(json_output)


def _parse_line(line: str) -> List[OperationDTO]:
    """Converts a JSON string line into a list of OperationDTOs."""
    operations_raw = json.loads(line)
    return [
        OperationDTO(
            operation=op["operation"],
            unit_cost=Decimal(str(op["unit-cost"])),
            quantity=op["quantity"],
        )
        for op in operations_raw
    ]


def _format_output(results: List[Dict[str, Any]]) -> str:
    """Formats the list of dictionaries back into a JSON string."""
    return json.dumps(results)