import numpy as np

a = np.arange(5 * 4 * 3 * 2, dtype=np.int32)
acc = np.zeros(5 * 4 * 3 * 2, dtype=np.int32)

r = a % 2
acc += r
a = a // 2

r = a % 3
acc += r*10
a = a // 3

r = a % 4
acc += r*100
a = a // 4

r = a % 5
acc += r*1000
a = a // 5

print(acc)
print(acc.reshape(5, 4, 3, 2))
#print(np.swapaxes(acc.reshape(5, 4, 3, 2), 1, 3))
print(np.moveaxis(acc.reshape(5, 4, 3, 2), 3, 1))
