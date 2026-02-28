nums = [5, 2, 8, 1]
result = sorted(nums, key=lambda x: x)
print(result)
# Output:
# [1, 2, 5, 8]



nums = [5, 2, 8, 1]
result = sorted(nums, key=lambda x: -x)
print(result)
# Output:
# [8, 5, 2, 1]



words = ["banana", "kiwi", "apple"]
result = sorted(words, key=lambda x: len(x))
print(result)
# Output:
# ['kiwi', 'apple', 'banana']



students = [("Ali", 90), ("Sara", 85), ("Bob", 95)]
result = sorted(students, key=lambda x: x[1])
print(result)
# Output:
# [('Sara', 85), ('Ali', 90), ('Bob', 95)]



students = [("Ali", 90), ("Sara", 85), ("Bob", 95)]
result = sorted(students, key=lambda x: x[1], reverse=True)
print(result)
# Output:
# [('Bob', 95), ('Ali', 90), ('Sara', 85)]
