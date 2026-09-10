"""Calculate compound interest from command-line inputs."""

import argparse


def calculate_compound_interest(
    principal: float, annual_rate: float, compounds_per_year: int, years: float
) -> tuple[float, float]:
    """Return the final amount and interest earned.

    annual_rate is expressed as a percentage, such as 5 for 5%.
    """
    final_amount = principal * (
        1 + annual_rate / 100 / compounds_per_year
    ) ** (compounds_per_year * years)
    return final_amount, final_amount - principal


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate compound interest. Annual rate is a percentage."
    )
    parser.add_argument("principal", type=float, help="Initial principal amount")
    parser.add_argument("annual_rate", type=float, help="Annual interest rate in percent")
    parser.add_argument("compounds_per_year", type=int, help="Number of compounding periods per year")
    parser.add_argument("years", type=float, help="Total investment time in years")
    args = parser.parse_args()

    if args.principal < 0:
        parser.error("principal must be non-negative")
    if args.annual_rate < 0:
        parser.error("annual_rate must be non-negative")
    if args.compounds_per_year <= 0:
        parser.error("compounds_per_year must be greater than zero")
    if args.years < 0:
        parser.error("years must be non-negative")

    final_amount, interest_earned = calculate_compound_interest(
        args.principal, args.annual_rate, args.compounds_per_year, args.years
    )
    print(f"Final amount: {final_amount:.2f}")
    print(f"Interest earned: {interest_earned:.2f}")


if __name__ == "__main__":
    main()
