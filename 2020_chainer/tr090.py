# - remove b
# - [done] remove unnecessary portion
# - change input vector length to 2
# - change output data for softmax, and use softmax

import numpy as np
import chainer
from chainer import training
from chainer import datasets, iterators, optimizers
from chainer import Link, Chain
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

model = L.Classifier(model, lossfun=F.sigmoid_cross_entropy)
model.compute_accuracy = False

optimizer = optimizers.SGD()
optimizer.setup(model)
updater = training.updaters.StandardUpdater(train_iter, optimizer, device=gpu_id)
trainer = training.Trainer(updater, (max_epoch, 'epoch'), out='tr080_result')

trainer.extend(extensions.LogReport())
trainer.extend(extensions.Evaluator(test_iter, model, device=gpu_id))
trainer.extend(extensions.PrintReport(['epoch', 'main/loss', 'validation/main/loss', 'elapsed_time']))

trainer.run()

print(model.predictor.l1.W)
print(model.predictor.l1.W.grad)
print(model.predictor.l1.b)
print(model.predictor.l1.b.grad)
