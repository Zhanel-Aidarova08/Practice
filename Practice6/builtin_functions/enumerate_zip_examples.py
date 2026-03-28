# enumerate_zip_examples.py
# Demonstrates: enumerate(), zip(), zip_longest(), and combined patterns

from itertools import zip_longest

fruits  = ["apple", "banana", "cherry", "date"]
prices  = [1.20, 0.50, 2.80, 3.50]
in_stock = [True, True, False, True]

# ── enumerate() — index + value pairs ────────────────────────────────────────
print("=== enumerate() ===")
for i, fruit in enumerate(fruits):
    print(f"  [{i}] {fruit}")

print("\nenumerate(start=1):")
for i, fruit in enumerate(fruits, start=1):
    print(f"  {i}. {fruit}")

# Practical: find index of element
target = "cherry"
found = [(i, v) for i, v in enumerate(fruits) if v == target]
print(f"\nIndex of '{target}': {found}")

# ── zip() — parallel iteration ───────────────────────────────────────────────
print("\n=== zip() ===")
for fruit, price in zip(fruits, prices):
    print(f"  {fruit:10} ${price:.2f}")

# zip with three iterables
print("\nWith stock status:")
for fruit, price, stock in zip(fruits, prices, in_stock):
    status = "✓" if stock else "✗"
    print(f"  {status} {fruit:10} ${price:.2f}")

# ── zip() → dict ─────────────────────────────────────────────────────────────
catalog = dict(zip(fruits, prices))
print(f"\nCatalog dict: {catalog}")

# ── zip_longest() — handles unequal lengths ───────────────────────────────────
print("\n=== zip_longest() ===")
letters = ["a", "b", "c"]
numbers = [1, 2, 3, 4, 5]
for pair in zip_longest(letters, numbers, fillvalue="–"):
    print(f"  {pair}")

# ── enumerate() + zip() combined ─────────────────────────────────────────────
print("\n=== enumerate() + zip() ===")
for i, (fruit, price) in enumerate(zip(fruits, prices), start=1):
    print(f"  {i}. {fruit:10} ${price:.2f}")

# ── Unzipping (reverse of zip) ────────────────────────────────────────────────
pairs = [("Alice", 90), ("Bob", 75), ("Carol", 88)]
print("\n=== Unzip ===")
names, scores = zip(*pairs)
print(f"Names : {names}")
print(f"Scores: {scores}")
print(f"Average score: {sum(scores) / len(scores):.1f}")

# ── Practical example: grade report ──────────────────────────────────────────
print("\n=== Grade Report ===")
students = ["Alice", "Bob", "Carol", "Dave"]
grades   = [92, 78, 85, 61]

for rank, (name, grade) in enumerate(
    sorted(zip(students, grades), key=lambda x: x[1], reverse=True),
    start=1,
):
    print(f"  #{rank} {name:8} — {grade}")
