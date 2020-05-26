'''
## Printing Right-angled Triangle using asterisk

This is a star right-angled triangle with base as 4.

```text
*
**
***
****
```

You are given a number *n*. We want to print the triangle with base *n*.

Hint: You may need to use nested loop. Inner loop will be printing stars in
a single row.

# Input Format:
You will be given an integer *n*.

# Constraints:
1 <= *n* <= 20

# Output Format:
Star triangle with base *n*.
'''
import random

def solve(n):
    output = []
    for x in range(1, n+1):
        output.append('*' * x)
    return '\n'.join(output)

def main():
    inputs = [4] + list(filter(lambda x: x != 4, range(1, 21)))
    return [(x, solve(x)) for x in inputs]

if __name__ == "__main__":
    print(main())
