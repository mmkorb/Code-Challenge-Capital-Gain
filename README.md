# Capital Gains Calculator (Code Challenge Solved)

This project is a command-line interface (CLI) application that calculates capital gains taxes for a given list of stock market operations. For the full challenge description, please refer to the [Challenge Document](challenge.md).

## Features

-   Calculates taxes based on a 20% rate on profits.
-   Handles `buy` and `sell` operations.
-   Correctly computes the **Weighted Average Cost (WAC)** across multiple buy operations.
-   Accumulates **losses** from unprofitable sales.
-   Deducts accumulated losses from future profits before calculating taxes.
-   Correctly applies the **tax exemption rule** for sales with a total value less than or equal to R$ 20,000.00.
-   Correctly handles specific edge cases from the specification, such as:
    -   Accumulating losses even on tax-exempt sales.
    -   *Not* using profits from tax-exempt sales to offset accumulated losses.
    -   Resetting the WAC when the share quantity drops to zero and a new buy operation occurs.

## Architectural Decisions

The application was built using a robust and scalable architecture to ensure maintainability, testability, and a clear separation of concerns.

### Clean Architecture

The project follows the principles of **Clean Architecture**, dividing the software into three distinct layers:

-   **`Domain`**: The core of the application. It contains the pure business logic (`TaxCalculatorService`) and the domain models (`Operation`, `TaxResult`). This layer is completely independent of any framework or external detail.
-   **`Application`**: This layer orchestrates the flow of data. It contains the Use Cases of the application (e.g., `CalculateTaxesFromOperationsUseCase`), which are responsible for coordinating the `Domain` layer to achieve a specific business goal.
-   **`Infrastructure`**: The outermost layer. It contains all the implementation details, such as the CLI (`Typer`), the Dependency Injection container setup, and the handlers for reading from `stdin` and writing to `stdout`.

This structure ensures that changes to external details (like switching from a CLI to a Web API) have zero impact on the core business logic.

### Domain-Driven Design (DDD)

We applied principles from **Domain-Driven Design** to ensure our code accurately models the business problem.

-   **Focus on the Domain:** The `Domain` layer was built first and treated as the most important part of the application.
-   **Ubiquitous Language:** We strived to use names and concepts from the problem description (e.g., `Operation`, `TaxResult`, `Weighted Average Cost`) directly in our domain models and services to create a shared, unambiguous language.
-   **Isolated Domain:** The `Domain` layer has no dependencies on other layers, ensuring the business logic remains pure and easy to test.

### Test-Driven Development (TDD)

The entire application was developed following a strict TDD methodology. We started with a high-level **acceptance test** for each feature, which failed initially. Then, we wrote focused **unit tests** to drive the implementation of the `Domain` logic, ensuring every business rule was correctly implemented in isolation before integrating it into the full application. This resulted in a comprehensive test suite and high confidence in the final code's correctness.

### Dependency Injection (DI)

To maintain the decoupling between layers, we used the Dependency Injection pattern. The `Domain` services are injected into the `Application` layer's Use Cases, and the Use Cases are injected into the `Infrastructure` layer's command handlers. This is managed by a DI container, which acts as a central "map" for constructing the application's services (the Composition Root).

## Frameworks and Libraries

The few external libraries were chosen deliberately to solve specific problems and improve the project's elegance and scalability, as encouraged by the challenge.

-   **`Typer`**: Used to build the Command-Line Interface. It was chosen over the native `argparse` module because it allows for a much cleaner, more declarative, and scalable way to define commands, especially in an application designed to grow. This avoids complex boilerplate and `if/elif` structures.
-   **`dependency-injector`**: This framework was chosen to manage the DI Container. It provides a clean, declarative way to define the application's object graph and automates the construction and injection of services, which is far more maintainable than manual injection in a growing application.
-   **`pytest`**: The de-facto standard for testing in Python. It was used for its powerful features like fixtures and test parametrization, which allowed us to easily test all specified scenarios in both acceptance and unit tests.

## Getting Started

### Prerequisites

-   Python 3.12.7

### Installation

1.  **Extract the provided `.zip` file**
2.  **Navigate to the project's root directory**
3.  **Create a virtual environment**:
    ```sh
    python -m venv .venv
    ```
4.  **Activate the virtual environment**:
    * On Windows (PowerShell):
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
    * On macOS/Linux (bash):
        ```sh
        source .venv/bin/activate
        ```
5.  **Install the project and its dependencies**:
    This project uses a modern Python packaging approach with `pyproject.toml` for configuration, following current best practices. Use the following command to install the package in editable mode along with development dependencies (such as `pytest`):
    ```sh
    pip install -e .[dev]
    ```

## Usage

### Running the Application

The application is a CLI that reads JSON-formatted stock operations from standard input (`stdin`). Each line is treated as an independent simulation. An empty line signals the end of the input.

**1. Manual Input (Pasting)**

Run the application:
* On Windows:
    ```
    Get-Content path/to/input.txt | python -m capital_gains_calculator
    ```
* On macOS/Linux:
    ```
    python -m capital_gains_calculator < path/to/input.txt
    ```

**2. Tests**

The project has a full suite of acceptance and unit tests. To run all tests, simply execute pytest in the root directory:
    ```
    pytest
    ```