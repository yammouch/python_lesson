import numpy as np

a = np.loadtxt("pr010.dat", dtype=np.float32)
print(a)

print(a.reshape( 2, 3, 4))
print(a.reshape(-1, 3, 4))
