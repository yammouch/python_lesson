#from __future__ import print_function

import argparse
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L

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
 '{}/results/416982/model_epoch-1000'.format(args.resultpath),
 model)

print('model.l1.W:', model.l1.W)
print('model.l1.b:', model.l1.b)

#for i in range(2):
#  # Show the output
#  x, t = test[i]
#  print('input:', x)
#  print('label:', t)

#  y = model(x[None, ...])

#  print('output:', y.data)
#  #print('predicted_label:', y.data.argmax(axis=1)[0])

#; lein run -m mlp.t0150-fw data/t0150_pr.dat

#(ns mlp.t0150-fw
#  (:gen-class)
#  (:require [clojure.pprint]
#            [mlp.mlp-jk :as mlp]
#            [mlp.meander]
#            [mlp.schemedit :as smp]))

#(defn make-schem []
#  (:field (first (mlp.meander/ring-0 [10 10] [4 4 3 3 1 2]))))
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
#for row in schem:
#  print(row.split(','))
#shamt = 1
#for row in schem:
#  print([(int('0' + x, 16) >> shamt) & 1 for x in row.split(',')])
schem_a = np.array([ [ [(int('0' + x, 16) >> shamt) & 1 for x in row.split(',')]
                       for row in schem ]
                     for shamt in range(6) ])
#print schem_a
for row in format_field(schem_a):
  print(row)
# - split by comma
# - 0 if space, or mask and shift, on 2d matrix
# - list comprehension
# - np.array

#(defn read-param [fname]
#  (let [[x & xs] (read-string (str "(" (slurp fname) ")"))]
#    [x (partition 2 xs)]))

#(defn set-param [param]
#  (dosync
#    (doseq [[i p] param]
#      (alter mlp/jk-mem #(assoc-in % [i :p] (float-array p)))
#      )))

#(defn split-output-vector [ns l]
#  (loop [[x & xs] ns, l l, acc []]
#    (if x
#      (recur xs (drop x l) (conj acc (take x l)))
#      acc)))

#(defn decode-one-hot [l]
#  (->> (map-indexed vector l)
#       (apply max-key #(% 1))
#       first))

#(defn parse-output-vector [l]
#  (mapv decode-one-hot (split-output-vector [2 10 10 10] l)))

#(defn format-field [field]
#  (mapv (fn [row]
#          (as-> row r
#                (map #(->> (reverse %)
#                           (reduce (fn [acc x] (+ (* acc 2) x)))
#                           (format "%02X"))
#                     r)
#                (interpose " " r)
#                (apply str r)))
#        field))

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

