class A:
    def method_a(self):
        print("A")

class B:
    def method_b(self):
        print("B")

class C(A, B):
    pass

c = C()
c.method_a()
c.method_b()
# Output:
# A
# B



class Father:
    def skills(self):
        print("Driving")

class Mother:
    def skills2(self):
        print("Cooking")

class Child(Father, Mother):
    pass

ch = Child()
ch.skills()
ch.skills2()
# Output:
# Driving
# Cooking



class X:
    def x(self):
        print("X")

class Y:
    def y(self):
        print("Y")

class Z(X, Y):
    pass

z = Z()
z.x()
z.y()
# Output:
# X
# Y



class A:
    def show(self):
        print("From A")

class B:
    def show2(self):
        print("From B")

class C(A, B):
    pass

c = C()
c.show()
c.show2()
# Output:
# From A
# From B



class One:
    def first(self):
        print("First")

class Two:
    def second(self):
        print("Second")

class Three(One, Two):
    pass

t = Three()
t.first()
t.second()
# Output:
# First
# Second
