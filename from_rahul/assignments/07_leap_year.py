'''
## Check whether a year is a leap year or not

You are given a year and you want to know whether it's a leap year or not.

A year is a leap year if it's a multiple of 4 except when it's a century then
that century is a leap year if it is a multiple of 400.

# Input Format:
You will be given an integer *x* as year.

# Constraints:
1 <= *x* <= 3000

# Output Format:
If it's a leap year then print "leap" otherwise "not leap"
'''

import random


def leap(y):
    if y % 100 == 0:
        return y % 400 == 0
    return y % 4 == 0

def print_leap(y):
    return "leap" if leap(y) else "not leap"

def main():
    tests = [(2020, print_leap(2020)), (2019, print_leap(2019))]
    random.seed(1234)
    for i in range(30):
        if random.random() < 0.33:
            y = random.randrange(100, 3000, 100)
        else:
            y = random.randint(1, 3000)
        tests.append((y, print_leap(y)))
    return tests

if __name__ == "__main__":
    main()
