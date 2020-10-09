'''
## Dot Product

You have given two *n* dimensional vectors. Your task is to find their dot product.

# Input Format:
You will be given two lines. Both containing a list of *n* floating point numbers separated by space.

# Constraints:
1 <= *n* <= 1000
-1000 <= value in the vector <= 1000

# Output Format:
A floating point number representing the dot product of the 2 vectors.
Print the floating point number up to six decimal places.
'''

import random

def solve(a, b):
    d = sum([x*y for x, y in zip(a, b)])
    return f"{d:0.6f}"

def main():
    random.seed(1234)
    inputs = [([1, 2, 1], [2, 2, 1])]

    for i in range(10):
        n = random.randrange(1, 10)
        a = [random.randrange(-10, 10) for _ in range(n)]
        b = [random.randrange(-10, 10) for _ in range(n)]
        inputs.append((a, b))
    for i in range(10):
        n = random.randrange(10, 1000)
        a = [random.random() for _ in range(n)]
        b = [random.random() for _ in range(n)]
        inputs.append((a, b))
    for i in range(10):
        n = random.randrange(10, 1000)
        a = [random.random()*2000-1000 for _ in range(n)]
        b = [random.random()*2000-1000 for _ in range(n)]
        inputs.append((a, b))
    return [([a, b], [solve(a, b)]) for a, b in inputs]

if __name__ == "__main__":
    print(main())
