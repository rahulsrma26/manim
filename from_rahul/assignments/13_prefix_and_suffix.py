'''
## Prefixes and Suffixes

Let's consider a string "python"

These are all the prefixes:

```text
p
py
pyt
pyth
pytho
python
```

And these are all the suffixes:
```text
python
 ython
  thon
   hon
    on
     n
```

You are given a string and you need to print all the prefixes and suffixes.

# Input Format:
You will be given an string *s*.

# Constraints:
1 <= *len(s)* <= 20

# Output Format:
All the prefixes and suffixes with spaces for missing characters.
'''
import random

def solve(s):
    output = []
    for i in range(1, len(s) + 1):
        output.append(s[:i])
    for i in range(1, len(s)):
        output.append(' ' * i + s[i:])
    return '\n'.join(output)

def main():
    # return solve("_1_2_3_4_5_6_7_8_9_")
    inputs = ["python", "a", "the", "in", "he she it they", "time", "write", "$$$$$", "aabraacadaabraa", "csglitz", "_1_2_3_4_5_6_7_8_9_"]
    return [(x, solve(x)) for x in inputs]

if __name__ == "__main__":
    print(main())
