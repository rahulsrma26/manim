'''
## Calculate grades given marks

Your professor tasks you with grading your juniors. He gave you this marking scheme

![image](https://s3.amazonaws.com/hr-assets/0/1586026609-082e364ae6-table.png)

There can some invalid numbers as well. If you encounter them you need to handle them well.

# Input Format:
An integer *x*

# Constraints:
-1000 <= *x* <= 1000

# Output Format:
If marks are greater than 100 then print "Overflow"

If marks are less than 0 then print "Underflow"

If marks are between 0 and 100 then print appropriate grade
'''

import random

def grade(m):
    if m > 100:
        return "Overflow"
    elif m >= 90:
        return "A"
    elif m >= 75:
        return "B"
    elif m >= 50:
        return "C"
    elif m >= 0:
        return "F"
    else:
        return "Underflow"

def main():
    tests = [(75, grade(75)), (105, grade(105))]
    random.seed(9)
    for i in range(30):
        m = random.randint(-10, 110)
        tests.append((m, grade(m)))
    return tests


if __name__ == "__main__":
    main()
