'''
## Vowel Count

Given a string you need to count number of vowels in it.

For example ```Extra``` has 2 vowels: E and a.

You can assume these character as vowels:
a, e, i, o, and u.

# Input Format:
You will be given an string *s*.

# Constraints:
1 <= *len(s)* <= 19

# Output Format:
A single integer representing number of vowels in *s*.
'''
import random

def solve(s):
    return sum([int(c in 'aeiou') for c in s.lower()])

def main():
    # return solve("Bienvenue")
    inputs = ["Extra", "welcome", "nice", "Who Is YOUR BOSS??", "AEIOUaeiou", "CS GLITZ", "Rythm", "come in", "Bienvenue", "Sh@hs", "csglitz", "ABCDEFGHIJIHGFEDCBA"]
    return [(x, solve(x)) for x in inputs]

if __name__ == "__main__":
    print(main())
