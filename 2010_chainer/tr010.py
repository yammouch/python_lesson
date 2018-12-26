#!/usr/bin/env python
import argparse

import chainer
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions


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


def main():
  batchsize = 100
  model = L.Classifier(MLP(100, 10))
  optimizer = chainer.optimizers.Adam()
  optimizer.setup(model)
  train, test = chainer.datasets.get_mnist()
  train_iter = chainer.iterators.SerialIterator(train, batchsize)
  d = next(train_iter)
  print(type(train))
  print(type(train[0]))
  print(type(d))
  print(len(d))
  print(d[0])
  print(d[1])


if __name__ == '__main__':
  main()
