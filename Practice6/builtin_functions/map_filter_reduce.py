# map_filter_reduce.py
# Demonstrates: map(), filter(), reduce(), len(), sum(), min(), max(), sorted()

from functools import reduce

numbers = [3, 7, 1, 9, 4, 6, 2, 8, 5]
words   = ["apple", "banana", "kiwi", "mango", "fig", "cherry"]

# ── Built-in aggregates ───────────────────────────────────────────────────────
print("=== Aggregates ===")
print(f"List    : {numbers}")
print(f"len()   : {len(numbers)}")
print(f"sum()   : {sum(numbers)}")
print(f"min()   : {min(numbers)}")
print(f"max()   : {max(numbers)}")
print(f"sorted(): {sorted(numbers)}")
print(f"sorted(reverse=True): {sorted(numbers, reverse=True)}")

# ── map() — transform every element ──────────────────────────────────────────
print("\n=== map() ===")
squares   = list(map(lambda x: x ** 2, numbers))
uppercased = list(map(str.upper, words))
print(f"Squares   : {squares}")
print(f"Uppercased: {uppercased}")

# map() with two iterables
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))
print(f"Pairwise sums {a} + {b} = {sums}")

# ── filter() — keep elements matching a condition ────────────────────────────
print("\n=== filter() ===")
evens      = list(filter(lambda x: x % 2 == 0, numbers))
long_words = list(filter(lambda w: len(w) > 4, words))
print(f"Even numbers : {evens}")
print(f"Long words   : {long_words}")

# ── reduce() — fold list into a single value ──────────────────────────────────
print("\n=== reduce() ===")
total   = reduce(lambda acc, x: acc + x, numbers)
product = reduce(lambda acc, x: acc * x, numbers)
longest = reduce(lambda a, b: a if len(a) >= len(b) else b, words)
print(f"Sum of {numbers} = {total}")
print(f"Product         = {product}")
print(f"Longest word    = '{longest}'")

# ── Chaining: filter → map → reduce ──────────────────────────────────────────
print("\n=== Chained: sum of squares of even numbers ===")
result = reduce(
    lambda acc, x: acc + x,
    map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers))
)
print(f"Numbers : {numbers}")
print(f"Evens   : {evens}")
print(f"Result  : {result}")

# ── Type conversions ──────────────────────────────────────────────────────────
print("\n=== Type conversions ===")
print(f"int('42')      = {int('42')}")
print(f"float('3.14')  = {float('3.14')}")
print(f"str(100)       = {str(100)!r}")
print(f"bool(0)        = {bool(0)}")
print(f"bool('hello')  = {bool('hello')}")
print(f"list((1,2,3))  = {list((1, 2, 3))}")
print(f"tuple([4,5,6]) = {tuple([4, 5, 6])}")
print(f"set([1,1,2,3]) = {set([1, 1, 2, 3])}")

# ── Type checking ─────────────────────────────────────────────────────────────
print("\n=== type() / isinstance() ===")
for val in [42, 3.14, "hi", True, [1, 2]]:
    print(f"  {val!r:12} → type: {type(val).__name__:8} | isinstance(int): {isinstance(val, int)}")
