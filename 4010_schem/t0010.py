#from __future__ import print_function

import argparse
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import schemedit as sce

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

def radix2(length, n):
  retval = []
  for i in range(length):
    retval.append(n & 1)
    n >>= 1
  return retval

def decode_one_hot(l):
  lens = [2, 10, 10, 10]
  acc = 0
  acc_list = []
  for i in lens:
    acc_list.append((l[0].array)[acc:acc+i].argmax())
    acc += i
  return acc_list

def fw(model, schem):
  schem_a = np.array([ [ [ cell[i] for cell in row ]
                         for row in schem_l ]
                       for i in range(6) ])
  cmd = decode_one_hot(model(schem_a[np.newaxis, ...].astype(np.float32)))
  if cmd[0] == 0:
    return sce.move_y(schem_l, cmd[1:3], cmd[3])
  else:
    return sce.move_x(schem_l, cmd[1:3], cmd[3])

class MLP(chainer.Chain):

  n_out = 32

  def __init__(self):
    super(MLP, self).__init__()
    with self.init_scope():
      self.l1 = L.Convolution2D(6, 3, 3, pad=1)
      self.l2 = L.Convolution2D(3, 3, 3, pad=1)
      self.l3 = L.Linear(None, self.n_out)

  def __call__(self, x):
    h1 = F.sigmoid(self.l1(x))
    h2 = F.sigmoid(self.l2(h1))
    return self.l3(F.reshape(h2, (-1, 3*10*10)))

parser = argparse.ArgumentParser()
parser.add_argument('--resultpath', '-r',
 default='location of the training result')
args = parser.parse_args()

model = MLP()
chainer.serializers.load_npz(
 #'{}/results/416982/model_epoch-1000'.format(args.resultpath),
 '{}/results/model_epoch-10'.format(args.resultpath),
 model)

schem = \
[ '  ,  ,  ,  ,  ,  ,  ,  ,  ,  ' ,
  '0A,02,02,02,  ,  ,  ,  ,  ,  ' ,
  '  ,  ,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,  ,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,  ,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,  ,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,03,02,02,03,02,20,  ,02,10' ,
  '  ,01,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,01,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,02,02,02,  ,  ,  ,  ,  ,  ' ]
schem_l = [ [radix2(6, int('0' + cell, 16)) for cell in row.split(',')]
            for row in schem ]

for row in format_field(np.moveaxis(np.array(fw(model, schem_l)), 2, 0)):
  print(row)
