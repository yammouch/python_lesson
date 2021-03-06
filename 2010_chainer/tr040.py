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
  batchsize = 100
  out = 'tr040_result'
  model = L.Classifier(MLP(10, 10))
  optimizer = chainer.optimizers.Adam()
  optimizer.setup(model)
  src = range(10)
  ars = [np.zeros(10, dtype=np.float32) for _ in src]
  for i in src:
    ars[i][i] = 1.0
  train = chainer.datasets.TupleDataset(ars, src)
  train_iter = chainer.iterators.SerialIterator(train, batchsize)
  test_iter = chainer.iterators.SerialIterator(train, batchsize,
                                               repeat=False, shuffle=False)
  updater = training.updaters.StandardUpdater(
    train_iter, optimizer, device=-1)
  trainer = training.Trainer(updater, (1, 'epoch'), out=out)
  trainer.extend(extensions.Evaluator(test_iter, model, device=-1))
  trainer.extend(extensions.dump_graph('main/loss'))
  trainer.extend(extensions.snapshot(), trigger=(1, 'epoch'))
  trainer.extend(extensions.LogReport())
  trainer.extend(extensions.PrintReport(
    ['epoch', 'main/loss', 'validation/main/loss',
     'main/accuracy', 'validation/main/accuracy', 'elapsed_time']))
  trainer.extend(extensions.ProgressBar())
  trainer.run()
  serializers.save_npz('{}/mlp.model'.format(out), model)
  serializers.save_npz('{}/mlp.state'.format(out), optimizer)


if __name__ == '__main__':
  main()
