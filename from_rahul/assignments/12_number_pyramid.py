'''
## Printing a number pyramid

This is a number pyramid with base 4.

```text
   1
  121
 12321
1234321
```

You are given a number *n*. We want to print the pyramid with base *n*.

Hint: You may need to use nested loop. Inner loop will be printing numbers in
a single row.

# Input Format:
You will be given an integer *n*.

# Constraints:
1 <= *n* <= 20

# Output Format:
Number pyramid with base *n*.
'''
import random

def solve(n):
    output = []
    for x in range(1, n + 1):
        s = ' ' * (n - x)
        for y in range(1, x):
            s += str(y)
        for y in range(x, 0, -1):
            s += str(y)
        output.append(s)
    return '\n'.join(output)

def main():
    inputs = [4] + list(filter(lambda x: x != 4, range(1, 21)))
    return [(x, solve(x)) for x in inputs]

if __name__ == "__main__":
    print(main())
