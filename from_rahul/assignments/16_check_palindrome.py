'''
## Check Palindrome

Given a string you need check whether it's a palindrome or not.

Palindrome is a word, phrase, or sequence that reads the same backwards as forwards.
e.g. ```madam``` and ```Nurses run```

# Input Format:
You will be given an string *s*. Containing only alphabets and spaces.

# Constraints:
1 <= *len(s)* <= 100

# Output Format:
A single string ```True``` if *s* is a palindrome or ```False``` otherwise.
'''
import random

def solve(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def main():
    # return solve("Bienvenue")
    inputs = [
        "Palindrome", "Nurses run",
        "madam", "Who Is YOUR BOSS", "CS GLITZ", "Rythm", "Shahs",
        "ABCDEFGHIJIHGFEDCBA", "11 11 11", "saippuakivikauppias", "Malayalam", "2",
        "Composing", "example", "again", "almost soml", "k k k x k",
        "Never odd or even", "We panic in a pew", "Wont lovers revolt now", "Sir I demand I am a maid named Iris",
        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z z y x w v u t s r q p o n m l k j i h g f e d c b a"
        ]
    return [(x, solve(x)) for x in inputs]

if __name__ == "__main__":
    print(main())
