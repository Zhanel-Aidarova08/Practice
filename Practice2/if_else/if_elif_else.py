# Example 1
score = 85
if score >= 90:
    print("A")
elif score >= 70:
    print("B")  # Output: B
else:
    print("C")

# Example 2
x = 0
if x > 0:
    print("Positive")
elif x < 0:
    print("Negative")
else:
    print("Zero")  # Output: Zero

# Example 3
num = 15
if num % 3 == 0 and num % 5 == 0:
    print("FizzBuzz")  # Output: FizzBuzz
elif num % 3 == 0:
    print("Fizz")
elif num % 5 == 0:
    print("Buzz")
