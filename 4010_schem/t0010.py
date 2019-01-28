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

def decode_one_hot(l):
  lens = [2, 10, 10, 10]
  acc = 0
  acc_list = []
  for i in lens:
    acc_list.append((l[0].array)[acc:acc+i].argmax())
    acc += i
  return acc_list

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
schem_a = np.array([ [ [(int('0' + x, 16) >> shamt) & 1 for x in row.split(',')]
                       for row in schem ]
                     for shamt in range(6) ])
for row in format_field(schem_a):
  print(row)
cmd = decode_one_hot(model(schem_a[np.newaxis, ...].astype(np.float32)))
print(cmd)


schem_l = [ [ list(cell) for cell in row ]
            for row in np.moveaxis(schem_a, 0, 2) ]
if cmd[0] == 0:
  editted = sce.move_y(schem_l, cmd[1:3], cmd[3])
else:
  editted = sce.move_x(schem_l, cmd[1:3], cmd[3])
for row in format_field(np.moveaxis(np.array(editted), 2, 0)):
  print(row)

#(defn fw [schem]
#  (mlp/fw (float-array (mapcat (partial apply concat) schem)))
#  (let [[cmd from-y from-x to] (parse-output-vector (:i (last @mlp/jk-mem)))]
#    (clojure.pprint/pprint [cmd from-y from-x to])
#    ((case cmd 1 smp/move-x 0 smp/move-y) schem [from-y from-x] to)))

#(defn edit1 [schem]
#  (clojure.pprint/pprint schem)
#  (loop [i 0
#         schem schem
#         schem-next (fw schem)]
#    (if (and (< i 100) schem-next)
#      (recur (+ i 1) schem-next (fw schem-next))
#      (clojure.pprint/pprint (format-field schem))
#      )))

#(defn main-loop [schems]
#  (doseq [s schems]
#    (edit1 s)))

#(defn -main [param-fname]
#  (let [schems [(make-schem)]
#        [mlp-config params] (read-param param-fname)]
#    (mlp/init mlp-config 0)
#    (set-param params)
#    (main-loop schems)))

