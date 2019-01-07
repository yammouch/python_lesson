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

np.random.seed(1)

batchsize = 2
inputs = np.array([[1.0], [-1.0]], dtype=np.float32)
outputs = np.array([[1], [0]], dtype=np.int8)

#batchsize = 1
#inputs = np.array([[1.0]], dtype=np.float32)
#outputs = np.array([[1]], dtype=np.int8)

train = chainer.datasets.TupleDataset(inputs, outputs) 
test = chainer.datasets.TupleDataset(inputs, outputs) 

train_iter = iterators.SerialIterator(train, batchsize)
test_iter = iterators.SerialIterator(test, batchsize, False, False)

class MLP(Chain):

    def __init__(self, n_out=1):
        super(MLP, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(None, n_out,
             initialW=np.array([[np.log(2)]], dtype=np.float32))

    def forward(self, x):
        return self.l1(x)

#gpu_id = 0  # Set to -1 if you use CPU
gpu_id = -1  # Set to -1 if you use CPU

model = MLP()
if gpu_id >= 0:
    model.to_gpu(gpu_id)

max_epoch = 1

# Wrap your model by Classifier and include the process of loss calculation within your model.
# Since we do not specify a loss function here, the default 'softmax_cross_entropy' is used.
#model = L.Classifier(model)
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
trainer = training.Trainer(updater, (max_epoch, 'epoch'), out='tr080_result')

from chainer.training import extensions

trainer.extend(extensions.LogReport())
trainer.extend(extensions.snapshot(filename='snapshot_epoch-{.updater.epoch}'))
trainer.extend(extensions.snapshot_object(model.predictor, filename='model_epoch-{.updater.epoch}'))
trainer.extend(extensions.Evaluator(test_iter, model, device=gpu_id))
trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'validation/main/loss', 'elapsed_time']))
trainer.extend(extensions.PlotReport(['main/loss', 'validation/main/loss'], x_key='epoch', file_name='loss.png'))
trainer.extend(extensions.dump_graph('main/loss'))

trainer.run()

print(model.predictor.l1.W)
print(model.predictor.l1.W.grad)
print(model.predictor.l1.b)
print(model.predictor.l1.b.grad)

import matplotlib.pyplot as plt

model = MLP()
serializers.load_npz('tr080_result/model_epoch-1', model)

print('model.l1.W:', model.l1.W)
print('model.l1.b:', model.l1.b)

for i in range(2):
  # Show the output
  x, t = test[i]
  print('input:', x)
  print('label:', t)

  y = model(x[None, ...])

  print('output:', y.data)
  #print('predicted_label:', y.data.argmax(axis=1)[0])
