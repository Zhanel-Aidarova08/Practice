class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        print("Woof")

d = Dog()
d.speak()
# Output:
# Woof



class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    def greet(self):
        print("Hi, I am a student")

s = Student()
s.greet()
# Output:
# Hi, I am a student



class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

b = B()
b.show()
# Output:
# B



class Vehicle:
    def move(self):
        print("Moving")

class Bike(Vehicle):
    def move(self):
        print("Bike is moving")

b = Bike()
b.move()
# Output:
# Bike is moving



class Parent:
    def info(self):
        print("Parent info")

class Child(Parent):
    def info(self):
        print("Child info")

c = Child()
c.info()
# Output:
# Child info
