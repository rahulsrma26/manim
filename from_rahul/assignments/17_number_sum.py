'''
## Number sum

Given a sequence of *n* numbers you need calculate it's sum.

# Input Format:
You will be given an int *n* representing total number of elements in the sequence.
Next n lines will contain an integer representing the number of the sequence.

# Constraints:
1 <= *n* <= 100
-1000 <= number in sequence <= 1000

# Output Format:
A single integer representing the sum of elements in the sequence.
'''
import random

def solve(n, *a):
    return sum(a)

def main():
    random.seed(1234)
    inputs = [[1, *[4]], [3, *[2, -4, 3]]]
    for i in range(10):
        n = random.randrange(2, 10)
        inputs.append([n, *[random.randrange(-10, 10) for _ in range(n)]])
    for i in range(20):
        n = random.randrange(10, 100)
        inputs.append([n, *[random.randrange(-1000, 1000) for _ in range(n)]])
    return [(x, solve(*x)) for x in inputs]

if __name__ == "__main__":
    print(main())
