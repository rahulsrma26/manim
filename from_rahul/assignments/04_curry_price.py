'''
## Calculate the curry price for customers.

You have opened a shop for spicy curry, serving a single dish. You always wanted
to do something for senior citizens. So, you put a 50% discount for anyone above
or equals to 60 years old. The original price of your curry dish is 100 rupees.

Since, it's a spicy curry, you are not allowing children below 5 years old.

Calculate curry price for customers of different ages.

Extra Challenge: Try to do this without using any control flow operations like if else.
You should do it only with arithmetic operators.

# Input Format:
You will be given an integer 'x' representing the age of your customer.

# Constraints:
5 <= x <= 100

# Output Format:
A single integer representing the price customer has to pay.
'''

def price(a):
    p = 100 - (a // 60) * 50
    return p

def main():
    inputs = [18] + list(range(5, 105, 5))
    tests = [(i, price(i)) for i in inputs]
    return tests

if __name__ == "__main__":
    print(main())
