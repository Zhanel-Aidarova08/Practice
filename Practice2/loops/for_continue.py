# Example 1
for i in range(5):
    if i == 2:
        continue
    print(i)
# Output:
# 0
# 1
# 3
# 4

# Example 2
for j in range(1, 6):
    if j % 2 == 0:
        continue
    print(j)
# Output:
# 1
# 3
# 5

# Example 3
for k in "ABCDE":
    if k == "C":
        continue
    print(k)
# Output:
# A
# B
# D
# E
