'''
## Convert the temperature from Fahrenheit to Celsius

You have a friend living in the USA. Whenever you call him he always told you
the temperature first. But the problem is that he is using Fahrenheit scale.
While you are familiar with Celsius.

So, in order to understand that you need to convert it.

# Input Format:
Input 'x' will be single integer containing the temperature in degree Fahrenheit.

# Constraints:
-459 <= x <= 1000

# Output Format:
There will be 2 outputs.

First line should only show the integer value (it should ignore the values after decimal).

Second line should output a float value with 2 decimal places.
'''

def to_celsius(x):
    return (x - 32)*5/9

def main():
    inputs = [32] + list(range(-459, 1000, 100))
    tests = []
    for i in inputs:
        val = to_celsius(i)
        outs = [int(val), f"{val:0.2f}"]
        tests.append((i, outs))
    return tests

if __name__ == "__main__":
    print(main())
