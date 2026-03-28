# The findall() Function

import re
txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)



import re
txt = "The rain in Spain"
x = re.findall("Portugal", txt)
print(x)

if (x):
  print("Yes, there is at least one match!")
else:
  print("No match")




# The search() Function

import re
txt = "The rain in Spain"
x = re.search("\s", txt)
print("The first white-space character is located in position:", x.start()) 



import re
txt = "The rain in Spain"
x = re.search("Portugal", txt)
print(x)




# The split() Function

import re
#Split the string at every white-space character:
txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)



import re
#Split the string at the first white-space character:
txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)




# The sub() Function

import re
#Replace all white-space characters with the digit "9":
txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)



import re
#Replace the first two occurrences of a white-space character with the digit 9:
txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)




# Match Object

import re
#The search() function returns a Match object:
txt = "The rain in Spain"
x = re.search("ai", txt)
print(x)
# <_sre.SRE_Match object; span=(5, 7), match='ai'>



# .span() returns a tuple containing the start-, and end positions of the match.

import re
#Search for an upper case "S" character in the beginning of a word, and print its position:
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span())
# (12, 17)



# .string returns the string passed into the function
import re
#The string property returns the search string:
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string)
# The rain in Spain



# .group() returns the part of the string where there was a match
import re
#Search for an upper case "S" character in the beginning of a word, and print the word:

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())






# 1.Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
import re
x = "ab abb abbb a"
s = re.findall(r"ab*", x)
print(s)

# 2.Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
import re
x = "ab abb abbb abbbb"
s = re.findall(r"ab{2,3}", x)
print(s)

# 3.Write a Python program to find sequences of lowercase letters joined with a underscore.
import re 
x="hello_world python_regex Hello_World"
s=re.findall(r"[a-z]+_[a-z]+", x)
print(s)

# 4.Write a Python program to find the sequences of one upper case letter followed by lower case letters.
import re
x = "Hello python Regex"
s = re.findall(r"[A-Z][a-z]+", x)
print(s)

# 5.Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
import re
x = "aab axxb acb a123b"
s = re.findall(r"a.*b", x)
print(s)

# 6.Write a Python program to replace all occurrences of space, comma, or dot with a colon.
import re
x = "Hello, world. Python is great"
s = re.sub(r"[ ,.]", ":", x)
print(s)

# 7.Write a python program to convert snake case string to camel case string.
import re
a = "hello_world_example"
s = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), a)
print(s)

# 8.Write a Python program to split a string at uppercase letters.
import re
x = "The Rain In Almaty"
s = re.split(r"[A-Z]", x)
print(s)

# 9.Write a Python program to insert spaces between words starting with capital letters.
import re
x = "TheRainInAlmaty"
s = re.split(r"(?=[A-Z])", x)
print(s)

# 10.Write a Python program to convert a given camel case string to snake case.
import re
a = "helloWorldExample"
s = re.sub(r"([A-Z])", r"_\1", a).lower()
print(s)