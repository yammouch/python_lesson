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
  test_iter = chainer.iterators.SerialIterator(test, batchsize,
                                               repeat=False, shuffle=False)
  updater = training.updaters.StandardUpdater(
    train_iter, optimizer, device=-1)
  trainer = training.Trainer(updater, (1, 'epoch'), out='result')
  trainer.extend(extensions.Evaluator(test_iter, model, device=-1))
  trainer.extend(extensions.dump_graph('main/loss'))
  trainer.extend(extensions.snapshot(), trigger=(1, 'epoch'))
  trainer.extend(extensions.LogReport())
  trainer.extend(extensions.PrintReport(
    ['epoch', 'main/loss', 'validation/main/loss',
     'main/accuracy', 'validation/main/accuracy', 'elapsed_time']))
  trainer.extend(extensions.ProgressBar())
  trainer.run()


if __name__ == '__main__':
  main()
