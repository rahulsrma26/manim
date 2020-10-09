'''
## Occurrence Count

You have given a list of *n* integers and *q* queries.

For each query you haven given a number and you have to count how many times that number appear in the list.

# Input Format:
You will be given a list of *n* integers in a line separated by space.
Next line will contains *q* integers as a query.

# Constraints:
1 <= *n*, *q* <= 1000
1 <= *q* <= 1000
-1000 <= value in the list or query <= 1000

# Output Format:
A list of *q* integers in a line separated by space.
'''

import random

def solve(a, q):
    return [a.count(x) for x in q]

def main():
    random.seed(1234)
    inputs = [([1, 2, 1, 4, 1, 2], [1, 2, 3])]

    for i in range(10):
        n = random.randrange(1, 10)
        a = [random.randrange(-10, 10) for _ in range(n)]
        nq = random.randrange(max(1, n-5), n+5)
        q = random.sample(a + [random.randrange(-10, 10) for _ in range(nq)], nq)
        inputs.append((a, q))
    for i in range(20):
        n = random.randrange(10, 100)
        a = [random.randrange(-1000, 1000) for _ in range(n//4)]
        while len(a) < n:
            r = n - len(a)
            if r <= 1:
                a.append(random.choice(a))
            elif r <= 3:
                a.append(random.choice(a))
                a.append(random.randrange(-1000, 1000))
            else:
                a.extend(random.sample(a, r // 4))
                a.extend([random.randrange(-1000, 1000) for _ in range(r//4)])
        u = list(set(a))
        nq = random.randrange(len(u), 2*len(u))
        q = random.sample(u + [random.randrange(-1000, 1000) for _ in u], nq)
        inputs.append((a, q))
    return [([x, q], [solve(x, q)]) for x, q in inputs]

if __name__ == "__main__":
    print(main())
