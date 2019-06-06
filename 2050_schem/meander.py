from copy import deepcopy
from functools import reduce
import schemprep as smp
import schemmlp as scp
import util as utl

def range_2d(end, from_p, to, o):
  if o in {'u', 'd'}:
    o = 0
  elif o in {'l', 'r'}:
    o = 1
  q = from_p[o]
  if not type(to) is int:
    to = to[o]
  if to < q:
    a = range(q + end - 1, to - 1, -1)
  else:
    a = range(q, to + end)
  retval = []
  for x in a:
    p = from_p[:]
    p[o] = x
    retval.append(p)
  return retval

def range_n(from_p, to, o):
  return range_2d(0, from_p, to, o)

def line(field, from_p, to, o):
  fld = deepcopy(field)
  for y, x in range_n(from_p, to, o):
    fld[y][x][o] = 1
  return fld

def lines(field, from_p, tos):
  fld = deepcopy(field)
  for p, o in tos:
    fld = line(fld, from_p, p, o)
    from_p = p
  return fld

def add_elements(field, els):
  fld = deepcopy(field)
  for p, d in els:
    fld[p[0]][p[1]][d] = 1
  return fld

#    |<-  l0  ->|
#   _            p1
#  |_>----------+  -
#    p0         |  ^
#               |  l1
#     p3      p2|  v
#   -  +--------+  -
#   ^  |<- l2 ->|
#  l3  |
#   v  |p4       |\  p6       _
#   -  +---------| >o--------|_>
#              p5|/         p7
#
#      |<- l4  ->|  |<- l5 ->|

def meander_0_points(l):
  y0 = l[1] + l[3]
  p0 = [-y0 if y0 < 0 else 0, 0]
  p1 = [ p0[0]       , p0[1] + l[0] ]
  p2 = [ p1[0] + l[1], p1[1]        ]
  p3 = [ p2[0]       , p2[1] - l[2] ]
  p4 = [ p3[0] + l[3], p3[1]        ]
  p5 = [ p4[0]       , p4[1] + l[4] ]
  p6 = [ p5[0]       , p5[1] +   2  ]
  p7 = [ p6[0]       , p6[1] + l[5] ]
  return [y0, p0, p1, p2, p3, p4, p5, p6, p7]

def meander_0_0(size, l):
  y0, p0, p1, p2, p3, p4, p5, p6, p7 = meander_0_points(l)
  fld = reduce(lambda acc, x: [deepcopy(acc) for _ in range(x)],
               [6] + size[::-1], 0)
  fld = add_elements(fld, [[p0, 3], [p5, 5], [p7, 4]])
  fld = lines(fld, p0, [[p1, 1], [p2, 0], [p3, 1], [p4, 0], [p5, 1]])
  fld = line(fld, p6, p7[1], 1)
  cmd = {'cmd': 'move-x',
         'org': [(p1[0] + p2[0]) // 2, p1[1]],
         'dst': p3[1]}
  return {'field': fld, 'cmd': cmd}

def meander_0_1(size, l):
  y0, p0, _, _, _, p4, p5, p6, p7 = meander_0_points(l)
  fld = reduce(lambda acc, x: [deepcopy(acc) for _ in range(x)],
               [6] + size[::-1], 0)
  fld = add_elements(fld, [[p0, 3], [p5, 5], [p7, 4]])
  fld = line(fld, p0, p4[1], 1)
  fld = lines(fld, [p0[0], p4[1]], [[p4, 0], [p5, 1]])
  fld = line(fld, p6, p7[1], 1)
  cmd = {'cmd': 'move-y',
         'org': p0,
         'dst': p4[0]}
  return {'field': fld, 'cmd': cmd}

def meander_0(size, l):
  return [meander_0_0(size, l), meander_0_1(size, l)]

#def meander_pos(n):
#  m = meander_0([14, 14], [4, 2, 2, 2, 4, 2])
#  u, d, l, r = smp.room(m[0]["field"])
#  print([u, d, l, r])
#  ml = [[dy, dx] for dy in range(-u, d+1) for dx in range(-l, r+1)]
#  ml = utl.select(ml, [n], utl.xorshift(2, 4, 6, 8))
#  ml = ml[0]
#  return [scp.slide_history(m, ml) for x in ml]

#    |<-  l0  ->|
#   _            p1
#  |_>----------+  -
#    p0         |  ^
#               |  l1
#     p4        |  v     |\            _
#      +--------+--------| >o---------|_>
#      |<- l3 ->|  ^   p5|/  p6     p7
#      |        |  l2
#      |p3    p2|  v
#      +--------+
#                <- l4 ->    <- l5 ->

def ring_0_points(l):
  y0 = l[1] + l[2]
  x0 = l[0] - l[3]
  p0 = [-y0 if y0 < 0 else 0, -x0 if x0 < 0 else 0]
  p1 = [ p0[0]              , p0[1] + l[0]        ]
  p2 = [ p1[0] + l[1] + l[2], p1[1]               ]
  p3 = [ p2[0]              , p2[1] - l[3]        ]
  p4 = [ p3[0] - l[2]       , p3[1]               ]
  p5 = [ p4[0]              , p4[1] + l[3] + l[4] ]
  p6 = [ p5[0]              , p5[1] +   2         ]
  p7 = [ p6[0]              , p6[1] + l[5]        ]
  return [p0, p1, p2, p3, p4, p5, p6, p7]

def ring_0_0(size, l):
  p0, p1, p2, p3, p4, p5, p6, p7 = ring_0_points(l)
  fld = reduce(lambda acc, x: [deepcopy(acc) for _ in range(x)],
               [6] + size[::-1], 0)
  fld = add_elements(fld, [[p0, 3], [p5, 5], [p7, 4]])
  fld = lines(fld, p0, [[p1, 1], [p2, 0], [p3, 1], [p4, 0], [p5, 1]])
  fld = line(fld, p6, p7[1], 1)
  cmd = {'cmd': 'move-y',
         'org': [p2[0], (p2[1] + p3[1])//2],
         'dst': p4[0]}
  return {'field': fld, 'cmd': cmd}

def ring_0_1(size, l):
  p0, p1, _, _, p4, p5, p6, p7 = ring_0_points(l)
  fld = reduce(lambda acc, x: [deepcopy(acc) for _ in range(x)],
               [6] + size[::-1], 0)
  fld = add_elements(fld, [[p0, 3], [p5, 5], [p7, 4], [[p4[0], p1[1]], 2]])
  fld = lines(fld, p0, [[p1, 1], [p4, 0], [p5, 1]])
  fld = line(fld, p6, p7[1], 1)
  cmd = {'cmd': 'move-x',
         'org': p4,
         'dst': p1[1]}
  return {'field': fld, 'cmd': cmd}

def ring_0_2(size, l):
  p0, p1, _, _, _, p5, p6, p7 = ring_0_points(l)
  fld = reduce(lambda acc, x: [deepcopy(acc) for _ in range(x)],
               [6] + size[::-1], 0)
  fld = add_elements(fld, [[p0, 3], [p5, 5], [p7, 4]])
  fld = lines(fld, p0, [[p1, 1], [[p5[0], p1[1]], 0], [p5, 1]])
  fld = line(fld, p6, p7[1], 1)
  cmd = {'cmd': 'move-y',
         'org': p0,
         'dst': p5[0]}
  return {'field': fld, 'cmd': cmd}

def ring_0(size, l):
  return [ring_0_0(size, l), ring_0_1(size, l), ring_0_2(size, l)]

#    |<-  l0  ->|  |<- l1 ->|
#
#   _           |\         p3
#  |_>----------| >o--------+  -
#     p0      p1|/  p2      |  ^
#                           |  l2
#                           |  v   p7 _
#                  p6+------+--------|_>
#                    |      |  ^
#                    |      |  l3
#                    |    p4|  v
#                  p5+------+  -
#
#                    |<-l4->|<- l5 ->|

def ring_1_points(l):
  y0 = l[2] + l[3]
  x0 = l[4] - l[0] - 2 - l[1]
  p0 = [-y0 if y0 < 0 else 0,
         x0 if 0 < x0 else 0]
  p1 = [p0[0]              , p0[1] + l[0]       ]
  p2 = [p1[0]              , p1[1] + 2          ]
  p3 = [p2[0]              , p2[1] + l[1]       ]
  p4 = [p3[0] + l[2] + l[3], p3[1]              ]
  p5 = [p4[0]              , p4[1] - l[4]       ]
  p6 = [p5[0] - l[3]       , p5[1]              ]
  p7 = [p6[0]              , p6[1] + l[4] + l[5]]
  return [p0, p1, p2, p3, p4, p5, p6, p7]

def ring_1_0(size, l):
  p0, p1, p2, p3, p4, p5, p6, p7 = ring_1_points(l)
  fld = reduce(lambda acc, x: [deepcopy(acc) for _ in range(x)],
               [6] + size[::-1], 0)
  fld = add_elements(fld, [[p0, 3], [p1, 5], [p7, 4]])
  fld = line(fld, p0, p1[1], 1)
  fld = lines(fld, p2, [[p3, 1], [p4, 0], [p5, 1], [p6, 0], [p7, 1]])
  cmd = {'cmd': 'move-y',
         'org': [p4[0], (p4[1] + p5[1])//2],
         'dst': p6[0]}
  return {'field': fld, 'cmd': cmd}

def ring_1_1(size, l):
  p0, p1, p2, p3, p4, p5, p6, p7 = ring_1_points(l)
  fld = reduce(lambda acc, x: [deepcopy(acc) for _ in range(x)],
               [6] + size[::-1], 0)
  fld = add_elements(fld, [[p0, 3], [p1, 5], [p7, 4], [[p6[0], p3[1]], 2]])
  fld = line(fld, p0, p1[1], 1)
  fld = lines(fld, p2, [[p3, 1], [p6, 0], [p7, 1]])
  cmd = {'cmd': 'move-x',
         'org': p6,
         'dst': p3[1]}
  return {'field': fld, 'cmd': cmd}

def ring_1_2(size, l):
  p0, p1, p2, p3, p4, p5, p6, p7 = ring_1_points(l)
  fld = reduce(lambda acc, x: [deepcopy(acc) for _ in range(x)],
               [6] + size[::-1], 0)
  fld = add_elements(fld, [[p0, 3], [p1, 5], [p7, 4]])
  fld = line(fld, p0, p1[1], 1)
  fld = lines(fld, p2, [[p3, 1], [[p6[0], p3[1]], 0], [p7, 1]])
  cmd = {'cmd': 'move-y',
         'org': p7,
         'dst': p3[0]}
  return {'field': fld, 'cmd': cmd}

def ring_1(size, l):
  return [ring_1_0(size, l), ring_1_1(size, l), ring_1_2(size, l)]

def position_variation(m, rs):
  u, d, l, r = smp.room(m[0]["field"])
  ml = [[dy, dx] for dy in range(-u, d+1) for dx in range(-l, r+1)]
  n = len(ml)
  mtr, mts = utl.select(ml, [n-1, 1], rs)
  return [[scp.slide_history(m, x) for x in ml],
 #return [[scp.slide_history(m, x) for x in mtr],
          [scp.slide_history(m, x) for x in mts]]

def meander_0_geometry_variation(size):
  return [meander_0(size, [g0+g2, g1, g2, g3, g4, g5])
          for g0 in [0]
          for g1, g3 in ( [(g1, g3) for g1 in [ 2,  3,  4] for g3 in [ 2]] +
                          [(g1, g3) for g1 in [-2, -3, -4] for g3 in [-2]] )
          for g2 in [2, 3, 4] for g4 in [2] for g5 in [2]]

def ring_0_geometry_variation(size):
  return [ring_0(size, [g0, g1, g2, g3, g4, g5])
          for g0 in [4]
          for g1, g2 in ( [(g1, g2) for g1 in [ 4] for g2 in [ 2,  3,  4]] +
                          [(g1, g2) for g1 in [-4] for g2 in [-2, -3, -4]] )
          for g3 in [2, 3, 4] for g4 in [1] for g5 in [2]]

def ring_1_geometry_variation(size):
  return [ring_1(size, [g0, g1, g2, g3, g4, g5])
          for g0 in [2] for g1 in [1]
          for g2, g3 in ( [(g2, g3) for g2 in [ 2] for g3 in [ 2,  3,  4]] +
                          [(g2, g3) for g2 in [-2] for g3 in [-2, -3, -4]] )
          for g4 in [2, 3, 4] for g5 in [2]]

def test_pattern(size):
  #histories = meander_0_geometry_variation(size)
  histories = ring_0_geometry_variation(size) \
            + ring_1_geometry_variation(size)
  # [h h ...]

  pvs = [position_variation(geom, utl.xorshift(2, 4, 6, 8))
         for geom in histories]
  # [ [[h h ...] [h h ...]]
  #   [[h h ...] [h h ...]]
  #   ... ]

  return list(zip(*pvs))
  # [ [[h h ...] [h h ...] ...]
  #   [[h h ...] [h h ...] ...] ]

#(defn -main []
#  (let [height 10, width 10
#        p (test-pattern [height width])
#        [tr ts] (map (comp (partial apply concat)
#                           (partial apply concat))
#                     p)
#        tr (mapv #(mlp.schemmlp/make-input-label % height width) tr)
#        ts (mapv #(mlp.schemmlp/make-input-label % height width) ts)]
#    (print-data tr :field "train_in.dat" )
#    (print-data tr :cmd   "train_out.dat")
#    (print-data ts :field "test_in.dat"  )
#    (print-data ts :cmd   "test_out.dat" )))

def main():
  for sequ in meander_0([14, 14], [4, 2, 2, 2, 4, 2]):
  #for sequ in ring_0([14, 14], [4, -2, -3, 3, 2, 2]):
  #for sequ in ring_1([14, 14], [2, 2, -2, -3, 3, 2]):
    print(utl.format_field(sequ["field"]))
    print('-' * 60)
  p = test_pattern([14, 14])
  print(len(p))
  print(len(p[0]))
  print(len(p[0][0]))
  print(len(p[0][0][0]))


if __name__ == '__main__':
  main()
