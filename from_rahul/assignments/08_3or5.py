'''
## Three or Five

You are given a number *n*. We want to calculate the count of all the numbers
between 1 and *n* that are divisible by either 3 or 5.

Extra Challenge: Try to do without using loops and if-else.

# Input Format:
You will be given an integer *n*.

# Constraints:
0 <= *n* <= 1000

# Output Format:
A single integer representing the count.
'''
import random

def count(x):
    return x // 3 + x // 5 - x // 15

def main():
    random.seed(1234)
    inputs = [5, 11]
    for i in range(20):
        inputs.append(random.randrange(100, 1000))
    return [(x, count(x)) for x in inputs]

if __name__ == "__main__":
    print(main())
