# Math and random operation
# 1.Write a Python program to convert degree to radian.
import math

degree = float(input("Input degree: "))
radian = degree * math.pi / 180

print("Output radian:", round(radian, 6))

# Input:
# 15
# Output:
# Output radian: 0.261799




# 2.Write a Python program to calculate the area of a trapezoid.
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = ((base1 + base2) / 2) * height

print("Expected Output:", area)

# Height: 5
# Base, first value: 5
# Base, second value: 6
# Expected Output: 27.5




# 3.Write a Python program to calculate the area of regular polygon.
import math

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

area = (n * s**2) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", round(area))

# Input number of sides: 4
# Input the length of a side: 25
# The area of the polygon is: 625




# 4.Write a Python program to calculate the area of a parallelogram.
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height

print("Expected Output:", area)

# Length of base: 5
# Height of parallelogram: 6
# Expected Output: 30.0