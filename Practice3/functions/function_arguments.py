def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")
# Emil Refsnes
# Tobias Refsnes
# Linus Refsnes



def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument
# Hello Email



def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")
# Email Refsnes




def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")
# Hello Emil
# Hello Tobias
# Hello friend
# Hello Linus



def my_function(country = "Norway"):
  print("I am from", country)

my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil")
# I am from Sweden
# I am from India
# I am from Norway
# I am from Brazil

