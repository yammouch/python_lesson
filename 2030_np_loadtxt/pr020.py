import numpy as np
import chainer.links.connection.convolution_2d as C

np.random.seed(1)

init_w = np.zeros([1, 1, 3, 2], dtype=np.float32)

l1 = C.Convolution2D(3, 2, initialW=init_w)
print(l1.W)
#print(l1.W.shape)
