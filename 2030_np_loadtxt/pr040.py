import numpy as np

a = np.loadtxt("../../jocl_lesson/0270_sasimi/train_in.dat", dtype=np.float32)
print(a.shape)
print(np.moveaxis(a.reshape(-1, 10, 10, 6), 3, 1).shape)
