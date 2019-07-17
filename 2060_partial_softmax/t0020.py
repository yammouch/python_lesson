import numpy as np
import chainer

x = chainer.Variable(np.array([1.0]))
y = x**2
print(y.debug_print())
y.backward(retain_grad=True)
print(y.debug_print())
print(y.grad)
