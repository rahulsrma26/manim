'''
## Simplified Tax Calculator

Your friend lives a country called Ninjaland. He needs your help in doing
taxes for him and his colleagues. The standard currency is called coin.

And here are the tax rules:

- If someone earns less than 100,000 yearly then he/she is exempted from tax.
- If annual income is more than or equals to 100,000 but less than 200,000 then the tax will be 10% of the annual income.
- If annual income is more than or equals to 200,000 but less than 500,000 then the tax will be 20% of the annual income.
- If annual income is more than or equals to 500,000 then he/she has to pay 30% of the annual income.
- If someone's tax contain decimal values then government will just ignore the decimal values as a discount and takes only integer part as a tax.

# Input Format:
You will be given an integer *x* representing the annual income in coins.

# Constraints:
0 <= *x* <= 1,000,000,000

# Output Format:
A single integer representing your annual income after tax deduction.
'''

import random

def after_tax(income):
    if income < 100_000:
        return income
    if income < 200_000:
        return income - int(income*0.10)
    if income < 500_000:
        return income - int(income*0.20)
    return income - int(income*0.30)

def main():
    inputs = [10_000, 200_007]
    for i in range(10):
        inputs.append(random.randrange(0, 200_000))
    for i in range(7):
        inputs.append(random.randrange(200_000, 1_000_000))
    for i in range(3):
        inputs.append(random.randrange(1_000_000, 1_000_000_000))
    tests = [(i, after_tax(i)) for i in inputs]
    return tests

if __name__ == "__main__":
    print(main())
