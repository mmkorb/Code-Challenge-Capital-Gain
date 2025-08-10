# tests/acceptance/test_cli_scenarios.py
# Acceptance tests that simulate user interaction via CLI.

import json
import subprocess
import sys
from pathlib import Path

import pytest

# Defines the path to the fixtures directory, relative to this test file.
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def run_application(input_data: str) -> str:
    """Runs the command-line application in a subprocess."""
    process = subprocess.run(
        [sys.executable, "-m", "capital_gains_calculator"],
        input=input_data,
        capture_output=True,
        text=True,
        check=False,
    )
    if process.stderr:
        print("Subprocess error:", process.stderr)
    return process.stdout


@pytest.mark.parametrize("case_number", [1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_acceptance_scenarios(case_number):
    """
    Tests the end-to-end acceptance scenarios.
    The 'parametrize' allows this same test to run for multiple cases.
    """
    # Arrange: Loads input and output data from fixture files.
    input_file = FIXTURES_DIR / f"case_{case_number}_input.txt"
    output_file = FIXTURES_DIR / f"case_{case_number}_output.json"

    # The input to the application is the content of the text file plus blank lines.
    input_data = input_file.read_text() + "\n\n"

    # The expected output is the content of the JSON file, loaded as a Python object.
    expected_output = json.loads(output_file.read_text())

    # Act: Runs the application with the input data.
    actual_output_str = run_application(input_data)

    # Assert: Checks if the output matches the expected output.
    actual_output = json.loads(actual_output_str)

    assert actual_output == expected_output
