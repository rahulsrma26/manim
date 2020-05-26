'''
## Convert from Centimeters to Feet and Inches

You have a measuring tape which can measure length in centimeter. You are using
this tape to measure your height. But in your job application form you need to
enter your height in feet and inches.

To calculate it you should use this formula:

1 inch = 2.54 centimeters

Write a program to convert from centimeter to feet and inches.

# Input Format:
Input 'x' will be single integer containing the height in centimeters.

e.g. 123

# Constraints:
1 <= x <= 300

# Output Format:
Output should be a string representing the feet with single quote and inches with
double quotes. Feet should be an integer while inches will a float with single decimal place.

e.g. 5'9.0"
'''

def to_feet_inches(cm):
    inches = cm / 2.54
    feet = inches // 12
    inches = inches - feet * 12
    return int(feet), inches

def main():
    inputs = [173] + list(range(1, 300, 20))
    tests = []
    for cm in inputs:
        f, i = to_feet_inches(cm)
        out = f"{f}'{i:.1f}\""
        tests.append((cm, out))
    return tests

if __name__ == "__main__":
    print(main())
