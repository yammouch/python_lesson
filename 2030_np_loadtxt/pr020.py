import numpy as np
import chainer.links as L

np.random.seed(1)

init_w = np.zeros([2, 3, 1, 1], dtype=np.float32)

#l1 = L.Convolution2D(3, 2, 1)
l1 = L.Convolution2D(3, 2, 1, initialW=init_w)
i1 = np.arange(1 * 3 * 5 * 4, dtype=np.float32).reshape(1, 3, 5, 4)
print(i1)
print(l1(i1))
print(l1.W)
print(l1.W.shape)
