from collections import defaultdict
import time
import numpy as np

words = {'apple', 'bat', 'bar', 'atom', 'book'}
by_letter = {}
# for word in words:
#     letter = word[0]
#     if letter in by_letter:
#         by_letter[letter].append(word)
#     else:
#         by_letter[letter] = [word]
# print(by_letter)

# for word in words:
#     letter = word[0]
#     by_letter.setdefault(letter, []).append(word)
# print(by_letter)

# by_letter = defaultdict(list)
# for word in words:
#     by_letter[word[0]].append(word)
# print(by_letter)


# def add_number(x, y):
#     return x + y


# add_five = lambda y: add_number(5, y)
# print(add_five(10))

# gen = (x**2 for x in range(10))
# with open("test.txt", 'a') as handle:
#     handle.writelines(str(x) + "\n" for x in gen)
# print(handle.closed)

my_arr = np.arange(1000000)
my_list = list(range(1000000))
start = time.process_time()
for _ in range(10):
    my_arr2 = my_arr * 2
end = time.process_time()
print((end - start) * 1000)

start = time.process_time()
for _ in range(10):
    my_list2 = [x * 2 for x in my_list]
end = time.process_time()
print((end - start) * 1000)