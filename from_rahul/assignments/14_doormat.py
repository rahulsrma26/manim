'''
## Designer Doormat

You got a request from a doormat manufacturing company. They want to create a
 pattern for the doormat. User can customize a pattern by his custom text.
The only condition is that the length of the text should be odd.

This is the doormat pattern for text "Welcome"

```text
-----------------
------..W..------
----....E....----
--......L......--
--W.E.L.C.O.M.E--
--......O......--
----....M....----
------..E..------
-----------------
```

Notice that if the length of the text is ```n``` then the width of the pattern
 will be ```2*n+3``` and the height will be ```n+2```. And all the characters are uppercase.

You are given a user text and you need to print the doormat pattern for it. If the length is
 not odd or it contains any characters other than letters then it should print "text not supported"

# Input Format:
You will be given an string *s*.

# Constraints:
1 <= *len(s)* <= 19

# Output Format:
Doormat pattern using the string characters, '-', and '.'.
'''
import random

def solve(s):
    n = len(s)
    if n % 2 == 0 or sum([c.isalpha() for c in s]) != n:
        return "text not supported"
    s = s.upper()
    n2 = int(n//2)
    w = 2*n+3
    output = [''.center(w, '-')]
    for i, c in enumerate(s[:n2]):
        output.append(('..'*(i+1) + c + '..'*(i+1)).center(w, '-'))
    output.append(('.'.join(s)).center(w, '-'))
    for i, c in enumerate(s[n2+1:]):
        output.append(('..'*(n2-i) + c + '..'*(n2-i)).center(w, '-'))
    output.append(''.center(w, '-'))
    return '\n'.join(output)

def main():
    # return solve("Bienvenue")
    inputs = ["WELCOME", "nice", "swaagat", "se7en", "Arigato", "CS GLITZ", "Rythm", "come in", "Bienvenue", "Sh@hs", "csglitz", "ABCDEFGHIJIHGFEDCBA"]
    return [(x, solve(x)) for x in inputs]

if __name__ == "__main__":
    print(main())
