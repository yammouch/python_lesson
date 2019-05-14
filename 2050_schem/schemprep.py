import util as utl
import copy
from functools import reduce

def format_field(field):
  fld = []
  for row in field
    r = []
    for c in row
      c = reduce(lambda acc, x: acc*2+x, c[::-1])
      c = '  ' if c == 0 else '{:02X}'.format(c)
      r.append(c)
    fld.append(','.join(r))
  return fld

def count_empty_row_up(field):
  i = 0
  while i < len(field) and all([all([x == 0 for x in c]) for c in field[i]])
    i += 1
  return i

def room(field):
  b = field[::-1]
  l = zip(*field)
  r = l[::-1]
  return [count_empty_row_up(x) for x in [field, b, l, r]]

#(defn slide-1d [field n o]
#  (let [empty (as-> field x
#                    (iterate first x)
#                    (take-while coll? x)
#                    (map count x)
#                    (drop (+ o 1) x)
#                    (reverse x)
#                    (reduce #(vec (repeat %2 %1)) 0 x))
#        fslide (fn [l] (vec (take (count l)
#                                  (concat (repeat n empty)
#                                          (drop (- n) l)
#                                          (repeat empty)))))]
#    (utl/mapd fslide o field)))

#(defn slide [field v]
#  (reduce (fn [fld [n o]] (slide-1d fld n o))
#          field
#          (map vector v (range))))

#(defn padding [rows h w]
#  (let [empty 0]
#    (as-> (concat rows (repeat [])) rows
#          (map (fn [row]
#                 (as-> (repeat empty) x
#                       (concat row x)
#                       (take w x)))
#               rows)
#          (take h rows))))
