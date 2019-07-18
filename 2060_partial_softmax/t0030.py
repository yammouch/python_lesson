import numpy as np
import chainer
import chainer.functions as F

def my_lossfun(x, t):
  return F.softmax_cross_entropy(x[:, 0:2], t[:, 0]) + \
         F.softmax_cross_entropy(x[:, 2:5], t[:, 1]) + \
         F.softmax_cross_entropy(x[:, 5: ], t[:, 2])

#v = chainer.Variable(np.arange(16, dtype=np.float32).reshape(2, 8))
v = chainer.Variable(np.array(
 [[0, 1,  2, 4, 6,  3, 6, 9],
  [4, 0, 10, 5, 0, 12, 6, 0]], dtype=np.float32))
t = np.array([[1, 2, 2], [0, 0, 0]])
l = my_lossfun(v, t)
print(l)
l.backward(retain_grad=True)
print(l.grad)
print(l.debug_print())
print(v.grad)
print(v.debug_print())

v = chainer.Variable(np.array([[2, 4, 6]], dtype=np.float32))
l = F.softmax_cross_entropy(v, np.array([2]))
l.backward(retain_grad=True)
print(l.grad)
print(l.debug_print())
print(v.grad)
print(v.debug_print())

v = chainer.Variable(np.array([[12, 6, 0]], dtype=np.float32))
l = F.softmax_cross_entropy(v, np.array([0]))
l.backward(retain_grad=True)
print(l.grad)
print(l.debug_print())
print(v.grad)
print(v.debug_print())
