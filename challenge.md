# Code Challenge: Capital Gains

This document outlines a technical challenge to implement a command-line interface (CLI) application that calculates taxes on financial market operations (stocks). The solution should be a standalone application.

## Input

The program will receive lists of stock market operations in JSON format from standard input (stdin), one list per line. Each operation object contains three fields:
- `operation`: The type of operation, either "buy" or "sell".
- `unit-cost`: The price per share with two decimal places.
- `quantity`: The number of shares traded.

The operations are provided in chronological order. Each line represents an independent simulation, and the program should not maintain state from one line to the next. The input ends with an empty line.

## Output

For each line of input, the program must return a list of JSON objects to standard output (stdout). Each object in the output list should have a single field:
- `tax`: The amount of tax paid for that specific operation.

The output list must have the same number of elements as the input list of operations.

## Business Rules

1.  **Tax Rate**: Tax is 20% on the profit from a "sell" operation. Profit is calculated when the selling price is greater than the weighted average cost of acquisition.
2.  **Weighted Average Cost**: When buying shares, the weighted average cost must be recalculated. The formula is: `new-weighted-average = ((current-quantity * current-weighted-average) + (purchased-quantity * purchase-value)) / (current-quantity + purchased-quantity)`.
3.  **Losses**: Losses occur when selling shares for less than the weighted average cost. No tax is paid on losses, but past losses should be used to offset future profits until the entire loss is deducted.
4.  **Tax Exemption**: No tax is paid if the total value of a sale (`unit-cost` x `quantity`) is equal to or less than R$ 20,000.00. However, accumulated losses should still be deducted from subsequent profits.
5.  **Buy Operations**: No tax is paid on "buy" operations.
6.  **Decimal Precision**: Decimal values should be rounded to two decimal places.

## Technical and Architectural Expectations

* **State Management**: The application's internal state must be explicitly managed in memory and should be empty when the application starts.
* **Testing**: Unit and integration tests are expected to ensure the solution's robustness and sustainability.
* **Simplicity**: The solution should be small, simple to understand, and easy to maintain.
* **Dependencies**: The use of open-source libraries (e.g., for JSON parsing) is allowed, but frameworks and unnecessary boilerplate code should be limited.
* **README**: The solution should include a `README.md` file with technical and architectural decisions, justification for any libraries used, and instructions for building, running, and testing the code.