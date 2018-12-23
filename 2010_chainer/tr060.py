import numpy as np
import chainer.links as L

l1 = L.Linear(4, 3)
print(l1(np.array([[0, 1, 2, 3]], np.float32)))
