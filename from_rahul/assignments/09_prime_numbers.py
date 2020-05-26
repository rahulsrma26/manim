'''
## Printing Prime Numbers

You are given a number *n*. We want to print all the prime numbers between
*1* and *n* (including).

Hint: You may need to use nested loop. Inner loop to check prime and outer loop
to iterate though all the values between *1* to *n*.

# Input Format:
You will be given an integer *n*.

# Constraints:
2 <= *n* <= 1000

# Output Format:
All the prime numbers between *1* to *n* separated by space.
'''
import random

def solve(n):
    nums = []
    for x in range(2, n + 1):
        for k in range(2, x):
            if x % k == 0:
                break
        else:
            nums.append(x)
    return ' '.join([str(x) for x in nums])

def main():
    random.seed(1234)
    inputs = [3, 10]
    for i in range(10):
        inputs.append(random.randrange(2, 100))
    for i in range(20):
        inputs.append(random.randrange(100, 1000))
    return [(x, solve(x)) for x in inputs]

if __name__ == "__main__":
    print(main())
