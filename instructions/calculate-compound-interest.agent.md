# Calculate Compound Interest

## When to use

Use this instruction when a user needs the final value of an investment or loan after periodic compounding, along with the interest earned. Use `tools/compound_interest.py` when the inputs are numeric and the calculation should be reproducible from the command line.

## Required inputs

Collect these values in order:

1. `principal`: initial amount, as a non-negative number.
2. `annual_rate`: annual interest rate as a percentage, such as `5` for 5%.
3. `compounds_per_year`: positive whole number of compounding periods per year.
4. `years`: total time in years, as a non-negative number.

## Invocation

From the repository root, run:

```text
python tools/compound_interest.py <principal> <annual_rate> <compounds_per_year> <years>
```

For example:

```text
python tools/compound_interest.py 1000 5 12 10
```

The command calculates compound interest using:

```text
final amount = principal * (1 + annual rate / 100 / compounds per year) ** (compounds per year * years)
interest earned = final amount - principal
```

The tool rejects negative principal, negative annual rate, negative years, and zero or negative compounding periods.

## Presenting results

Report both output values exactly as returned by the tool:

```text
Final amount: 1647.01
Interest earned: 647.01
```

Keep the labels clear, preserve two decimal places, and state the input assumptions when they matter, especially that the annual rate is a percentage and how often interest compounds. Do not present the final amount as interest earned; interest earned is the final amount minus the principal.
