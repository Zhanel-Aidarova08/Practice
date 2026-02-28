nums = [1, 2, 3, 4, 5]
result = list(filter(lambda x: x % 2 == 0, nums))
print(result)
# Output:
# [2, 4]



nums = [10, 15, 20, 25]
result = list(filter(lambda x: x > 15, nums))
print(result)
# Output:
# [20, 25]



words = ["apple", "hi", "banana"]
result = list(filter(lambda x: len(x) > 3, words))
print(result)
# Output:
# ['apple', 'banana']



nums = [-2, -1, 0, 1, 2]
result = list(filter(lambda x: x > 0, nums))
print(result)
# Output:
# [1, 2]



names = ["Ali", "Bob", "Anara"]
result = list(filter(lambda x: x.startswith("A"), names))
print(result)
# Output:
# ['Ali', 'Anara']
