'''
## Sorting

Given a list of *n* words you need to sort them in dictionary order (ignoring case) and then print them in lower case.

# Input Format:
You will be given a list of *n* words in a line separated by space.

# Constraints:
2 <= *n* <= 100
1 <= length of the words <= 20

# Output Format:
A sorted list of the words in a line separated by space.
'''

import os
import random

def solve(a):
    return sorted([x.lower() for x in a])

def main():
    random.seed(1234)
    inputs = [['nice', 'Cheese', 'cake'], ['Aa', 'a', 'Abc']]

    fname = os.path.join(os.path.dirname(__file__), 'words.txt')
    words = [x.strip() for x in open(fname, 'r').readlines()]
    words = [x.upper() if random.random() < 0.5 else x.lower() for x in words]
    for i in range(10):
        inputs.append(random.sample(words, random.randrange(2, 10)))
    for i in range(10):
        inputs.append(random.sample(words, random.randrange(10, 100)))
    return [([x], [solve(x)]) for x in inputs]

if __name__ == "__main__":
    print(main())
