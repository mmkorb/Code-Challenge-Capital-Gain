from decimal import Decimal

# These imports will fail because the domain files have not been created yet
from capital_gains_calculator.domain.models import Operation, TaxResult
from capital_gains_calculator.domain.services import TaxCalculatorService


def test_calculate_taxes_for_exempt_operations():
    """
    Tests Case #1 scenario: one purchase followed by two sales,
    all exempt from tax.
    The domain service should calculate the tax correctly for this case.
    """
    # Arrange
    operations = [
        Operation(operation="buy", unit_cost=Decimal("10.00"), quantity=100),
        Operation(operation="sell", unit_cost=Decimal("15.00"), quantity=50),
        Operation(operation="sell", unit_cost=Decimal("15.00"), quantity=50),
    ]
    expected_taxes = [
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
    ]
    service = TaxCalculatorService()

    # Act
    actual_taxes = service.process(operations)

    # Assert
    assert actual_taxes == expected_taxes


def test_calculate_tax_for_profitable_sale_above_exemption_limit():
    """
    Tests tax calculation for a single sale with profit
    and total value above the exemption limit of 20,000 BRL.
    """
    # Arrange
    # Buy at 10.00, sell at 20.00. Profit of 10.00 per share.
    # Total sale: 5000 * 20.00 = 100000.00 (> 20000.00)
    # Total profit: 5000 * 10.00 = 50000.00
    # Tax due: 50000.00 * 20% = 10000.00
    operations = [
        Operation(operation="buy", unit_cost=Decimal("10.00"), quantity=10000),
        Operation(operation="sell", unit_cost=Decimal("20.00"), quantity=5000),
    ]
    expected_taxes = [
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("10000.00")),
    ]
    service = TaxCalculatorService()

    # Act
    actual_taxes = service.process(operations)

    # Assert
    assert actual_taxes == expected_taxes


def test_should_deduct_previous_losses_from_current_profit():
    """
    Tests deduction of accumulated losses from future profits.
    Scenario:
    1. Buy at 10.00, resulting in average price of 10.00.
    2. Sell at 5.00, generating a loss of 25,000. Tax is 0.
    3. Sell at 20.00, generating profit of 30,000.
    Taxable profit should be 5,000 (30k - 25k), resulting in 1,000 tax.
    """
    # Arrange
    operations = [
        Operation(operation="buy", unit_cost=Decimal("10.00"), quantity=10000),
        Operation(operation="sell", unit_cost=Decimal("5.00"), quantity=5000),
        Operation(operation="sell", unit_cost=Decimal("20.00"), quantity=3000),
    ]
    expected_taxes = [
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("1000.00")),
    ]
    service = TaxCalculatorService()

    # Act
    actual_taxes = service.process(operations)

    # Assert
    assert actual_taxes == expected_taxes


def test_wac_is_calculated_correctly_with_multiple_buys():
    """
    Tests Weighted Average Cost (WAC) calculation with
    multiple purchases, as in Case #4.
    Average Price = ((10000 * 10) + (5000 * 25)) / 15000 = 15.00
    Sale at 15.00 should generate neither profit nor loss.
    """
    # Arrange
    operations = [
        Operation(operation="buy", unit_cost=Decimal("10.00"), quantity=10000),
        Operation(operation="buy", unit_cost=Decimal("25.00"), quantity=5000),
        Operation(operation="sell", unit_cost=Decimal("15.00"), quantity=10000),
    ]
    expected_taxes = [
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
    ]
    service = TaxCalculatorService()

    # Act
    actual_taxes = service.process(operations)

    # Assert
    assert actual_taxes == expected_taxes


def test_scenario_with_zero_profit_sale_followed_by_profitable_sale():
    """
    Tests Case #5 scenario: Multiple purchases, one sale with no profit,
    and a final profitable sale, ensuring service state
    (average price and remaining shares) is maintained correctly.
    """
    # Arrange
    operations = [
        Operation(operation="buy", unit_cost=Decimal("10.00"), quantity=10000),
        Operation(operation="buy", unit_cost=Decimal("25.00"), quantity=5000),
        Operation(operation="sell", unit_cost=Decimal("15.00"), quantity=10000),
        Operation(operation="sell", unit_cost=Decimal("25.00"), quantity=5000),
    ]
    expected_taxes = [
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("10000.00")),
    ]
    service = TaxCalculatorService()

    # Act
    actual_taxes = service.process(operations)

    # Assert
    assert actual_taxes == expected_taxes


def test_loss_from_exempt_sale_is_accumulated_and_used():
    """
    Tests Case #6 scenario, where a loss generated in an
    exempt sale (total value <= 20k) is accumulated and used to
    offset profits from future non-exempt sales.
    """
    # Arrange
    operations = [
        Operation(operation="buy", unit_cost=Decimal("10.00"), quantity=10000),
        # Sale with loss of 40k, but exempt (total value 10k)
        Operation(operation="sell", unit_cost=Decimal("2.00"), quantity=5000),
        # Sale with profit of 20k, remaining loss 20k
        Operation(operation="sell", unit_cost=Decimal("20.00"), quantity=2000),
        # Sale with profit of 20k, loss zeroed out
        Operation(operation="sell", unit_cost=Decimal("20.00"), quantity=2000),
        # Sale with profit of 15k, tax on 15k = 3k
        Operation(operation="sell", unit_cost=Decimal("25.00"), quantity=1000),
    ]
    expected_taxes = [
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("3000.00")),
    ]
    service = TaxCalculatorService()

    # Act
    actual_taxes = service.process(operations)

    # Assert
    assert actual_taxes == expected_taxes


def test_full_lifecycle_with_stock_reset_from_case_7():
    """
    Tests the full scenario of Case #7, which includes resetting the
    stock position and then starting a new buy and sell cycle,
    which should reset the weighted average price.
    """
    # Arrange
    operations = [
        Operation(operation="buy", unit_cost=Decimal("10.00"), quantity=10000),
        Operation(operation="sell", unit_cost=Decimal("2.00"), quantity=5000),
        Operation(operation="sell", unit_cost=Decimal("20.00"), quantity=2000),
        Operation(operation="sell", unit_cost=Decimal("20.00"), quantity=2000),
        Operation(operation="sell", unit_cost=Decimal("25.00"), quantity=1000),
        # Stock reset. New purchase sets a new average price of 20.00.
        Operation(operation="buy", unit_cost=Decimal("20.00"), quantity=10000),
        # Sale with loss of 25k.
        Operation(operation="sell", unit_cost=Decimal("15.00"), quantity=5000),
        # Sale with profit of 43.5k, deducting loss. Tax on 18.5k = 3.7k
        Operation(operation="sell", unit_cost=Decimal("30.00"), quantity=4350),
        # Sale with profit of 6.5k, but exempt (total value 19.5k). Tax 0.
        Operation(operation="sell", unit_cost=Decimal("30.00"), quantity=650),
    ]
    expected_taxes = [
        TaxResult(tax=Decimal("0.00")),  # buy
        TaxResult(tax=Decimal("0.00")),  # sell with loss
        TaxResult(tax=Decimal("0.00")),  # sell deducts loss
        TaxResult(tax=Decimal("0.00")),  # sell deducts loss
        TaxResult(tax=Decimal("3000.00")),  # sell deducts loss and profits
        TaxResult(tax=Decimal("0.00")),  # buy
        TaxResult(tax=Decimal("0.00")),  # sell with loss
        TaxResult(tax=Decimal("3700.00")),  # sell deducts loss and profits
        TaxResult(tax=Decimal("0.00")),  # sell with profit but exempt
    ]
    service = TaxCalculatorService()

    # Act
    actual_taxes = service.process(operations)

    # Assert
    assert actual_taxes == expected_taxes


def test_wac_resets_after_selling_all_shares():
    """
    Tests Case #8 scenario, ensuring that the Weighted Average Cost
    resets after all shares are sold.
    """
    # Arrange
    operations_part1 = [
        Operation(operation="buy", unit_cost=Decimal("10.00"), quantity=10000),
        Operation(operation="sell", unit_cost=Decimal("50.00"), quantity=10000),
    ]
    # After the first part, shares are zeroed out. Previous WAC of 10.00 is discarded.
    operations_part2 = [
        Operation(operation="buy", unit_cost=Decimal("20.00"), quantity=10000),
        Operation(operation="sell", unit_cost=Decimal("50.00"), quantity=10000),
    ]

    # Process the first part
    service = TaxCalculatorService()
    service.process(operations_part1)

    # Act: Process the second part, which should operate with a new WAC of 20.00
    actual_taxes = service.process(operations_part2)

    # Profit from second sale = (50 - 20) * 10000 = 300000
    # Tax = 300000 * 0.20 = 60000
    expected_taxes = [
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("60000.00")),
    ]

    # Assert
    assert actual_taxes == expected_taxes


def test_complex_scenario_from_case_9_with_all_rules():
    """
    Tests the full scenario of Case #9, which involves interaction of
    all business rules:
    - Multiple purchases with varied prices.
    - Loss on sale with exempt total value (20k BRL), which should be accumulated.
    - Profit on sale with exempt total value, which should not offset the loss.
    - Profit on non-exempt sale that offsets accumulated loss.
    - Final profit without loss to offset.
    """
    # Arrange
    operations = [
        Operation(operation="buy", unit_cost=Decimal("5000.00"), quantity=10),
        Operation(operation="sell", unit_cost=Decimal("4000.00"), quantity=5),
        Operation(operation="buy", unit_cost=Decimal("15000.00"), quantity=5),
        Operation(operation="buy", unit_cost=Decimal("4000.00"), quantity=2),
        Operation(operation="buy", unit_cost=Decimal("23000.00"), quantity=2),
        Operation(operation="sell", unit_cost=Decimal("20000.00"), quantity=1),
        Operation(operation="sell", unit_cost=Decimal("12000.00"), quantity=10),
        Operation(operation="sell", unit_cost=Decimal("15000.00"), quantity=3),
    ]
    expected_taxes = [
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("0.00")),
        TaxResult(tax=Decimal("1000.00")),
        TaxResult(tax=Decimal("2400.00")),
    ]
    service = TaxCalculatorService()

    # Act
    actual_taxes = service.process(operations)

    # Assert
    assert actual_taxes == expected_taxes
