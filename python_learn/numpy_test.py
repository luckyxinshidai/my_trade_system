import numpy as np
import random
import matplotlib.pyplot as plt
import sys

# position = 0
# walk = [position]
# steps = 1000
# for i in range(steps):
#     step = 1 if random.randint(0, 1) else -1
#     position += step
#     walk.append(position)
#
# plt.plot(walk[:100])
# plt.pause(15)
# plt.close()
# arr = np.arange(10)
# nsteps = 100
# draws = np.random.randint(0, 2, size=nsteps)
# # print(draws)
# steps = np.where(draws > 0, 1, -1)
# walk = steps.cumsum()
# print(walk)
# plt.plot(walk[:100])
# plt.pause(15)
# plt.close()
# print(walk.max())
# print(walk.min())
# n = (np.abs(walk) >= 10).argmax()
# print(np.abs(walk) >= 10)
# print(n)

nwalks = 5000
nsteps = 1000
draws = np.random.randint(0, 2, size=(nwalks, nsteps))
# print(draws)
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1)
print(walks)
print(walks.max())
print(walks.min())

