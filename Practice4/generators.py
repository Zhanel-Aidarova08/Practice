# Iterator and generator exercises
# 1.Create a generator that generates the squares of numbers up to some number N.
def square_generator(n):
    for i in range(n + 1):
        yield i * i

n = int(input())
for value in square_generator(n):
    print(value)

# Input:
# 5
# Output:
# 0
# 1
# 4
# 9
# 16
# 25




# 2.Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input())
print(",".join(map(str, even_numbers(n))))

# Input:
# 10
# Output:
# 0,2,4,6,8,10




# 3.Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i

n = int(input())
for num in divisible_by_3_and_4(n):
    print(num)

# Input:
# 50
# Output:
# 0
# 12
# 24
# 36
# 48




# 4.Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

a = int(input())
b = int(input())

for value in squares(a, b):
    print(value)

# Input:
# 2
# 5
# Output:
# 4
# 9
# 16
# 25




# 5.Implement a generator that returns all numbers from (n) down to 0.
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input())
for num in countdown(n):
    print(num)

# Input:
# 5
# Output:
# 5
# 4
# 3
# 2
# 1
# 0

