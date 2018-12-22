#!/usr/bin/env python
import argparse

import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training, serializers
from chainer.training import extensions


# Network definition
class MLP(chainer.Chain):

  def __init__(self, n_units, n_out):
    super(MLP, self).__init__()
    with self.init_scope():
      # the size of the inputs to each layer will be inferred
      self.l1 = L.Linear(None, n_units)  # n_in -> n_units

  def forward(self, x):
    return F.relu(self.l1(x))


def main():
  model = L.Classifier(MLP(10, 10))
  serializers.load_npz('tr040_result/mlp.model', model)

  src = range(10)
  ars = [np.zeros(10, dtype=np.float32) for _ in src]
  for i in src:
    ars[i][i] = 1.0

  print(ars[0])
  with chainer.using_config('train', False), chainer.using_config('enable_backprop', False):
    print(model(ars[0]))
    #print(model(ars[1]))


if __name__ == '__main__':
  main()
