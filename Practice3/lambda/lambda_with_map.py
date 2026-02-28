nums = [1, 2, 3]
result = list(map(lambda x: x * 2, nums))
print(result)
# Output:
# [2, 4, 6]



nums = [1, 2, 3]
result = list(map(lambda x: x + 5, nums))
print(result)
# Output:
# [6, 7, 8]



nums = [2, 4, 6]
result = list(map(lambda x: x ** 2, nums))
print(result)
# Output:
# [4, 16, 36]



words = ["a", "b"]
result = list(map(lambda x: x.upper(), words))
print(result)
# Output:
# ['A', 'B']



nums = [10, 20]
result = list(map(lambda x: x - 1, nums))
print(result)
# Output:
# [9, 19]
