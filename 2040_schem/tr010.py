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

batchsize = 128
midN = 100

dataset = [np.loadtxt("../../jocl_lesson/0270_sasimi/{}.dat".format(x),
                      dtype=np.float32)
           for x in ["train_in", "train_out", "test_in", "test_out"]]

train = chainer.datasets.TupleDataset(dataset[0], dataset[1].astype(np.int8))
test = chainer.datasets.TupleDataset(dataset[2], dataset[3].astype(np.int8))

train_iter = iterators.SerialIterator(train, batchsize)
test_iter = iterators.SerialIterator(test, batchsize, False, False)

class MLP(Chain):

    def __init__(self, n_mid_units=100, n_out=32):
        print('n_mid_units={}'.format(n_mid_units))
        print('n_out={}'.format(n_out))
        super(MLP, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(None, n_out)

    def forward(self, x):
        return F.relu(self.l1(x))
        #return self.l2(h1)

#gpu_id = 0  # Set to -1 if you use CPU
gpu_id = -1  # Set to -1 if you use CPU

model = MLP(midN, 32)
if gpu_id >= 0:
    model.to_gpu(gpu_id)

max_epoch = 3

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
trainer = training.Trainer(updater, (max_epoch, 'epoch'), out='tr010_result')

from chainer.training import extensions

trainer.extend(extensions.LogReport())
trainer.extend(extensions.snapshot(filename='snapshot_epoch-{.updater.epoch}'))
trainer.extend(extensions.snapshot_object(model.predictor, filename='model_epoch-{.updater.epoch}'))
trainer.extend(extensions.Evaluator(test_iter, model, device=gpu_id))
trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'main/accuracy', 'validation/main/loss', 'validation/main/accuracy', 'elapsed_time']))
trainer.extend(extensions.PlotReport(['main/loss', 'validation/main/loss'], x_key='epoch', file_name='loss.png'))
trainer.extend(extensions.PlotReport(['main/accuracy', 'validation/main/accuracy'], x_key='epoch', file_name='accuracy.png'))
trainer.extend(extensions.dump_graph('main/loss'))

trainer.run()

import matplotlib.pyplot as plt

model = MLP(midN, 32)
serializers.load_npz('tr010_result/model_epoch-2', model)

print('model.l1.W:', model.l1.W)
print('model.l1.b:', model.l1.b)

for i in range(maxN):
  # Show the output
  x, t = test[i]
  print('input:', x)
  print('label:', t)

  y = model(x[None, ...])

  print('output:', y.data)
  print('predicted_label:', y.data.argmax(axis=1)[0])
