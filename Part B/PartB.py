from functools import reduce

######################## Q1
fib = lambda n: (lambda a=[0, 1]: a[:n] + [a.append(a[-1] + a[-2]) or a[-1] for _ in range(2, n)])()


######################## Q2
cat = lambda strings: reduce(lambda x, y: x + ' ' + y, strings)


######################## Q3
sum_squared_lists = lambda lists: list(map(lambda sublist: reduce(lambda acc, num: acc + num**2, filter(lambda x: x % 2 == 0, sublist), 0), lists))


######################## Q4
c_op = lambda op: lambda seq: reduce(lambda x, y: op(x, y), seq)


######################## Q5
def sum_squared_original(nums):
    nums = [1,2,3,4,5,6]
    evens = []
    for num in nums:
        if num % 2 == 0:
            evens.append(num)
    squared = []
    for even in evens:
        squared.append(even**2)

    sum_squared = 0
    for x in squared:
        sum_squared += x
    return(sum_squared)

sum_squared = lambda nums: reduce(lambda acc, x: acc + x, map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))


######################## Q6
palindromes = lambda lists: list(map(lambda sublist: len(list(filter(lambda s: s == s[::-1], sublist))), lists))


######################## Q7
def q7():
    def generate_values():
        print('Generating values...')
        yield 1
        yield 2
        yield 3

    def square(x):
        print(f'Squaring {x}')
        return x * x
    print('Eager evaluation:')
    values = list(generate_values())
    squared_values = [square(x) for x in values]
    print(squared_values)
    print('\nLazy evaluation:')
    squared_values = [square(x) for x in generate_values()]
    print(squared_values)


######################## Q8
prime_desc = lambda lst: sorted([x for x in lst if all(x % i != 0 for i in range(2, int(x**0.5) + 1)) and x > 1], reverse=True)


######################## EXAMPLE USAGE

print("\n------------------------ Q1")
print(fib(10))
print("Expected output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]")

print("\n------------------------ Q2")
print(cat(["Hello", "world", "this", "is", "Python"]))
print("Expected output: Hello world this is Python")

print("\n------------------------ Q3")
print(sum_squared_lists([[1, 2, 3, 4], [4, 5, 6], [7, 8, 9]]))
print("Expected output: [20, 52, 64]")

print("\n------------------------ Q4")
fact = c_op(lambda x, y: x * y)
print(fact(range(1, 6)))
print("Expected output: 120")
exp = lambda base, exp: c_op(lambda x, y: x * y)([base] * exp)
print(exp(2, 3))
print("Expected output: 8")

print("\n------------------------ Q5")
nums = [1, 2, 3, 4, 5, 6]
print(f"Original: {sum_squared_original(nums)}")
print(f"Modified: {sum_squared(nums)}")
print("Expected output: Both should be 56")

print("\n------------------------ Q6")
print(palindromes([["madonna", "madam", "racecar"], ["leave", "deified", "hello"]]))
print("Expected output: [2, 1]")

print("\n------------------------ Q7")
q7()
print("\nLazy Evaluation generates and squares values one at a time, delaying the computation until each value is required by the program")
print("as Eager Evaluation causes all values to be generated and stored in memory at once, and then squared.")

print("\n------------------------ Q8")
print(prime_desc([10, 11, 13, 14, 17, 229]))
print("Expected output: [229, 17, 13, 11]")