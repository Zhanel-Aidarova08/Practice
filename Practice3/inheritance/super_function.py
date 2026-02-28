class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age

s = Student("Ali", 18)
print(s.name, s.age)
# Output:
# Ali 18



class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        super().speak()
        print("Woof")

d = Dog()
d.speak()
# Output:
# Animal sound
# Woof



class A:
    def show(self):
        print("A method")

class B(A):
    def show(self):
        super().show()
        print("B method")

b = B()
b.show()
# Output:
# A method
# B method



class Parent:
    def __init__(self):
        print("Parent constructor")

class Child(Parent):
    def __init__(self):
        super().__init__()
        print("Child constructor")

c = Child()
# Output:
# Parent constructor
# Child constructor



class Vehicle:
    def move(self):
        print("Moving")

class Car(Vehicle):
    def move(self):
        super().move()
        print("Car is moving")

c = Car()
c.move()
# Output:
# Moving
# Car is moving
