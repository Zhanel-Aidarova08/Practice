class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()
# Output:
# Animal sound



class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    pass

s = Student()
s.greet()
# Output:
# Hello



class Vehicle:
    def move(self):
        print("Moving")

class Car(Vehicle):
    pass

c = Car()
c.move()
# Output:
# Moving



class Parent:
    def show(self):
        print("Parent method")

class Child(Parent):
    pass

ch = Child()
ch.show()
# Output:
# Parent method



class A:
    def method(self):
        print("From A")

class B(A):
    pass

b = B()
b.method()
# Output:
# From A
