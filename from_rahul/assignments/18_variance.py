'''
## Variance

Given a sequence of *n* numbers you need calculate it's variance.

The variance is the average of the sum of squares of the difference from mean.

Let's assume the *n* numbers are:

A1, A2, A3, ..., An

Their mean will be:

m = (A1 + A2 + A3 + ... + An) / n

and their variance will be

v = ((A1-m)**2 + (A2-m)**2 + (A3-m)**2 + ... + (An-m)**2) / (n - 1)

# Input Format:
You will be given an *n* integers in a line separated by space.

# Constraints:
2 <= *n* <= 100
-1000 <= number in sequence <= 1000

# Output Format:
A floating point number representing the variance of the sequence.
Print the floating point number up to six decimal places.
'''
import random
import statistics

def solve(a):
    m = sum(a) / len(a)
    v = sum([(x-m)**2 for x in a]) / (len(a) - 1)
    a = f"{statistics.variance(a):.6f}"
    b = f"{v:.6f}"
    if a != b:
        print("NOOOOOOOOOOOOOOOOOOOOOOOOOO", a, b)
    return a

def main():
    random.seed(1234)
    inputs = [[4, 4], [2, -2, 3]]
    for i in range(10):
        n = random.randrange(2, 10)
        inputs.append([random.randrange(-10, 10) for _ in range(n)])
    for i in range(20):
        n = random.randrange(10, 100)
        inputs.append([random.randrange(-1000, 1000) for _ in range(n)])
    return [([x], solve(x)) for x in inputs]

if __name__ == "__main__":
    print(main())
