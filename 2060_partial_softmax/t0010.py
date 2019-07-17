import numpy as np
import chainer
import chainer.functions as F

v = chainer.Variable(np.array([0.0, 0.0, np.log(2.0)], dtype=np.float32))
print(v)
v = F.reshape(v, (1, 3))
print(v)
#l = F.softmax_cross_entropy(v, np.array([0]))
#print(l)
#l = F.softmax_cross_entropy(v, np.array([1]))
#print(l)
l = F.softmax_cross_entropy(v, np.array([2]))
print(l.debug_print())
print(l)
#l.backward(None, 1.0)
l.backward(retain_grad=True)
#print(l.debug_print())
#print(v.debug_print())
print(l.grad)
print(v.grad)
