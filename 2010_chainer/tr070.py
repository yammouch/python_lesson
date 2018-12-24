#!/usr/bin/env python
import argparse

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import serializers

import matplotlib.pyplot as plt


# Network definition
class MLP(chainer.Chain):

  def __init__(self, n_units, n_out):
    super(MLP, self).__init__()
    with self.init_scope():
      # the size of the inputs to each layer will be inferred
      self.l1 = L.Linear(None, n_units)  # n_in -> n_units
      self.l2 = L.Linear(None, n_units)  # n_units -> n_units
      self.l3 = L.Linear(None, n_out)  # n_units -> n_out

  def forward(self, x):
    h1 = F.relu(self.l1(x))
    h2 = F.relu(self.l2(h1))
    return self.l3(h2)


model = L.Classifier(MLP(100, 10))
serializers.load_npz('tr000_result/model_epoch-1', model)

# Show the output
x, t = test[0]
plt.imshow(x.reshape(28, 28), cmap='gray')
plt.show()
print('label:', t)

y = model(x[None, ...])

print('predicted_label:', y.data.argmax(axis=1)[0])
