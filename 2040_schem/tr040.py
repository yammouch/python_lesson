import numpy as np
import chainer
from chainer import backend
from chainer import backends
from chainer.backends import cuda
from chainer import Function, gradient_check, report, training, utils, Variable
from chainer import datasets, iterators, optimizers, serializers
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L
from chainer.training import extensions

def format_field(ar):
  acc = np.zeros(ar.shape[1:])
  for i in range(ar.shape[0]):
    acc += ar[i] * 2**i
  sacc = []
  for i in range(ar.shape[1]):
    line = ','.join(['  ' if x == 0 else '{:02X}'.format(int(x))
                    for x in acc[i]])
    sacc.append(line)
  return sacc

np.random.seed(1)

batchsize = 128
midN = 100

dataset = [np.loadtxt("../../jocl_lesson/0270_sasimi/{}.dat".format(x),
                      dtype=np.float32)
           for x in ["train_in", "train_out", "test_in", "test_out"]]

#train = chainer.datasets.TupleDataset(dataset[0], dataset[1].astype(np.int8))
#test = chainer.datasets.TupleDataset(dataset[2], dataset[3].astype(np.int8))
train = chainer.datasets.TupleDataset(
 np.moveaxis(dataset[0].reshape(-1, 10, 10, 6), 3, 1),
 dataset[1].astype(np.int8) )
test = chainer.datasets.TupleDataset(
 np.moveaxis(dataset[2].reshape(-1, 10, 10, 6), 3, 1),
 dataset[3].astype(np.int8) )

train_iter = iterators.SerialIterator(train, batchsize)
test_iter = iterators.SerialIterator(test, batchsize, False, False)

pairs = next(train_iter)

#print(len(pairs))
#print(len(pairs[0]))
#print(pairs[0])
#print(pairs[0][0])
#print(len(pairs[1]))
#print(pairs[1])

for i in range(3):
  for line in format_field(pairs[i][0]):
    print(line)
  print(pairs[i][1][0:2].argmax())
  print(pairs[i][1][2:12].argmax())
  print(pairs[i][1][12:22].argmax())
  print(pairs[i][1][22:32].argmax())

class MLP(Chain):

  n_out = 32

  def __init__(self):
    super(MLP, self).__init__()
    with self.init_scope():
      self.l1 = L.Convolution2D(6, 3, 3, pad=1)
      self.l2 = L.Convolution2D(3, 3, 3, pad=1)
      self.l3 = L.Linear(None, self.n_out)

  def forward(self, x):
    h1 = F.sigmoid(self.l1(x))
    h2 = F.sigmoid(self.l2(h1))
    return self.l3(F.reshape(h2, (-1, 3*10*10)))

gpu_id = -1  # Set to -1 if you use CPU

model = MLP()

max_epoch = 10000

# Wrap your model by Classifier and include the process of loss calculation within your model.
# Since we do not specify a loss function here, the default 'softmax_cross_entropy' is used.
model = L.Classifier(model, lossfun=F.sigmoid_cross_entropy)
model.compute_accuracy = False

# selection of your optimizing method
#optimizer = optimizers.MomentumSGD()
optimizer = optimizers.SGD()

# Give the optimizer a reference to the model
optimizer.setup(model)

# Get an updater that uses the Iterator and Optimizer
updater = training.updaters.StandardUpdater(train_iter, optimizer, device=gpu_id)

# Setup a Trainer
trainer = training.Trainer(updater, (max_epoch, 'epoch'), out='tr030_result')

from chainer.training import extensions

trainer.extend(extensions.LogReport())
trainer.extend(extensions.snapshot(filename='snapshot_epoch-{.updater.epoch}'))
trainer.extend(extensions.snapshot_object(model.predictor, filename='model_epoch-{.updater.epoch}'))
trainer.extend(extensions.Evaluator(test_iter, model, device=gpu_id))
trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'main/accuracy', 'validation/main/loss', 'validation/main/accuracy', 'elapsed_time']))
trainer.extend(extensions.PlotReport(['main/loss', 'validation/main/loss'], x_key='epoch', file_name='loss.png'))
trainer.extend(extensions.PlotReport(['main/accuracy', 'validation/main/accuracy'], x_key='epoch', file_name='accuracy.png'))
trainer.extend(extensions.dump_graph('main/loss'))

#trainer.run()

import matplotlib.pyplot as plt

model = MLP()
serializers.load_npz('tr030_result/model_epoch-2', model)

print('model.l1.W:', model.l1.W)
print('model.l1.b:', model.l1.b)

for i in range(1):
  # Show the output
  x, t = test[i]
  print('input:', x)
  print('label:', t)

  y = model(x[None, ...])

  print('output:', y.data)
  #print('predicted_label:', y.data.argmax(axis=1)[0])
