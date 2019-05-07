import copy

#(ns mlp.meander
#  (:require [mlp.util :as utl]
#            [mlp.schemprep :as smp]
#            [mlp.schemmlp  :as scp]
#            [clojure.pprint]))

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
  fld = copy.deepcopy(field)
  for y, x for range_n(from_p, to, o):
    fld[y][x][o] = 1

def lines(field, from_p, tos):
  fld = copy.deepcopy(field)
  for p, o in tos:
    fld = line(fld, from_p, p, o)
  return fld

def add_elements(field, els):
  fld = copy.deepcopy(field)
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
  fld = [ [ [0] * 6 for _ in range(size[1]) ]
            for _ in range(size[0]) ]
  fld = add_elements(fld, [[p0, 3], [p5, 5], [p7, 4]])
  fld = lines(fld, p0, [[p1, 1], [p2, 0], [p3, 1], [p4, 0], [p5, 1]])
  fld = line(fld, p6, p7[1], 1)
  cmd = {'cmd': 'move-x',
         'org': [(p1[0] + p2[0]) // 2, p1[1]]
         'dst': p3[1]}
  return {'field': fld, 'cmd': cmd}

def meander_0_1(p, l):
  y0, p0, _, _, _, p4, p5, p6, p7 = meander_0_points(l)
  fld = [ [ [0] * 6 for _ in range(size[1]) ]
            for _ in range(size[0]) ]
  fld = add_elements(fld, [[p0, 3], [p5, 5], [p7, 4]])
  fld = line(fld, p0, p4[1], 1)
  fld = lines(fld, [p0[0], p4[1]], [[p4, 0], [p5, 1]])
  fld = line(fld, p6, p7[1], 1)
  cmd = {'cmd': 'move-y',
         'org': p0
         'dst': p4[0]}
  return {'field': fld, 'cmd': cmd}

#(def meander-0 (juxt meander-0-0 meander-0-1))

#(defn meander-pos [n]
#  (let [m (vec (meander-0 [14 14] [4 2 2 2 4 2]))
#        [u d l r] (smp/room (get-in m [0 :field]))
#        _ (println [u d l r])
#        ml (for [dy (range (- u) (+ d 1)) dx (range (- l) (+ r 1))]
#             [dy dx])
#        [ml] (utl/select (vec ml) [n] (utl/xorshift 2 4 6 8))]
#    (mapv (partial scp/slide-history m) ml)))

#;    |<-  l0  ->|
#;   _            p1
#;  |_>----------+  -
#;    p0         |  ^
#;               |  l1
#;     p4        |  v     |\            _
#;      +--------+--------| >o---------|_>
#;      |<- l3 ->|  ^   p5|/  p6     p7
#;      |        |  l2
#;      |p3    p2|  v
#;      +--------+
#;                <- l4 ->    <- l5 ->

#(defn ring-0-points [l]
#  (let [y0 (+ (l 1) (l 2))
#        x0 (- (l 0) (l 3))
#        p0 [(if (< y0 0) (- y0) 0)
#            (if (< x0 0) (- x0) 0)]
#        p1 (update-in p0 [1] + (l 0))
#        p2 (update-in p1 [0] + (l 1) (l 2))
#        p3 (update-in p2 [1] - (l 3))
#        p4 (update-in p3 [0] - (l 2))
#        p5 (update-in p4 [1] + (l 3) (l 4))
#        p6 (update-in p5 [1] + 2)
#        p7 (update-in p6 [1] + (l 5))]
#    [p0 p1 p2 p3 p4 p5 p6 p7]))

#(defn ring-0-0 [[h w] l]
#  (let [[p0 p1 p2 p3 p4 p5 p6 p7] (ring-0-points l)]
#   {:field
#    (as-> (reduce #(vec (repeat %2 %1)) 0 [6 w h]) fld
#          (add-elements fld [[p0 3] [p5 5] [p7 4]])
#          (lines fld p0 [[p1 1] [p2 0] [p3 1] [p4 0] [p5 1]])
#          (line fld p6 (p7 1) 1))
#    :cmd {:cmd :move-y
#          :org [(p2 0)
#                (quot (+ (p2 1) (p3 1)) 2)]
#          :dst (p4 0)}}))

#(defn ring-0-1 [[h w] l]
#  (let [[p0 p1 _ _ p4 p5 p6 p7] (ring-0-points l)]
#   {:field
#    (as-> (reduce #(vec (repeat %2 %1)) 0 [6 w h]) fld
#          (add-elements fld [[p0 3] [p5 5] [p7 4] [[(p4 0) (p1 1)] 2]])
#          (lines fld p0 [[p1 1] [p4 0] [p5 1]])
#          (line fld p6 (p7 1) 1))
#    :cmd {:cmd :move-x
#          :org p4
#          :dst (p1 1)}}))

#(defn ring-0-2 [[h w] l]
#  (let [[p0 p1 _ _ _ p5 p6 p7] (ring-0-points l)]
#   {:field
#    (as-> (reduce #(vec (repeat %2 %1)) 0 [6 w h]) fld
#          (add-elements fld [[p0 3] [p5 5] [p7 4]])
#          (lines fld p0 [[p1 1] [[(p5 0) (p1 1)] 0] [p5 1]])
#          (line fld p6 (p7 1) 1))
#    :cmd {:cmd :move-y
#          :org p0
#          :dst (p5 0)}}))

#(def ring-0 (juxt ring-0-0 ring-0-1 ring-0-2))

#;    |<-  l0  ->|  |<- l1 ->|
#;
#;   _           |\         p3
#;  |_>----------| >o--------+  -
#;     p0      p1|/  p2      |  ^
#;                           |  l2
#;                           |  v   p7 _
#;                  p6+------+--------|_>
#;                    |      |  ^
#;                    |      |  l3
#;                    |    p4|  v
#;                  p5+------+  -
#;
#;                    |<-l4->|<- l5 ->|

#(defn ring-1-points [l]
#  (let [y0 (+ (l 2) (l 3))
#        x0 (- (l 4) (l 0) 2 (l 1))
#        p0 [(if (< y0 0) (- y0) 0)
#            (if (< 0 x0) x0 0)]
#        p1 (update-in p0 [1] + (l 0))
#        p2 (update-in p1 [1] + 2)
#        p3 (update-in p2 [1] + (l 1))
#        p4 (update-in p3 [0] + (l 2) (l 3))
#        p5 (update-in p4 [1] - (l 4))
#        p6 (update-in p5 [0] - (l 3))
#        p7 (update-in p6 [1] + (l 4) (l 5))]
#    [p0 p1 p2 p3 p4 p5 p6 p7]))

#(defn ring-1-0 [[h w] l]
#  (let [[p0 p1 p2 p3 p4 p5 p6 p7] (ring-1-points l)]
#   {:field
#    (as-> (reduce #(vec (repeat %2 %1)) 0 [6 w h]) fld
#          (add-elements fld [[p0 3] [p1 5] [p7 4]])
#          (line fld p0 (p1 1) 1)
#          (lines fld p2 [[p3 1] [p4 0] [p5 1] [p6 0] [p7 1]]))
#    :cmd {:cmd :move-y
#          :org [(p4 0)
#                (quot (+ (p4 1) (p5 1)) 2)]
#          :dst (p6 0)}}))

#(defn ring-1-1 [[h w] l]
#  (let [[p0 p1 p2 p3 p4 p5 p6 p7] (ring-1-points l)]
#   {:field
#    (as-> (reduce #(vec (repeat %2 %1)) 0 [6 w h]) fld
#          (add-elements fld [[p0 3] [p1 5] [p7 4] [[(p6 0) (p3 1)] 2]])
#          (line fld p0 (p1 1) 1)
#          (lines fld p2 [[p3 1] [p6 0] [p7 1]]))
#    :cmd {:cmd :move-x
#          :org p6
#          :dst (p3 1)}}))

#(defn ring-1-2 [[h w] l]
#  (let [[p0 p1 p2 p3 p4 p5 p6 p7] (ring-1-points l)]
#   {:field
#    (as-> (reduce #(vec (repeat %2 %1)) 0 [6 w h]) fld
#          (add-elements fld [[p0 3] [p1 5] [p7 4]])
#          (line fld p0 (p1 1) 1)
#          (lines fld p2 [[p3 1] [[(p6 0) (p3 1)] 0] [p7 1]]))
#    :cmd {:cmd :move-y
#          :org p7
#          :dst (p3 0)}}))

#(def ring-1 (juxt ring-1-0 ring-1-1 ring-1-2))

#(defn -main []
#  ;(doseq [sequ (ring-0 [14 14] [4 -2 -3 3 2 2])]
#  (doseq [sequ (ring-1 [14 14] [2 2 -2 -3 3 2])]
#  ;(doseq [sequ (meander-0 [14 14] [4 2 2 2 4 2])]
#    (clojure.pprint/pprint
#     (smp/format-field (:field sequ)))
#    (clojure.pprint/pprint (:cmd sequ))
#    ))
#; lein run -m mlp.t0160-gentr

#(ns mlp.t0160-gentr
#  (:gen-class)
#  (:require [clojure.pprint]
#            [mlp.util :as utl]
#            [mlp.schemmlp]
#            [mlp.schemprep :as spp]
#            [mlp.meander]))

#(defn position-variation [m rs]
#  (let [m (vec m)
#        [u d l r] (spp/room (get-in m [0 :field]))
#        ml (for [dy (range (- u) (+ d 1)) dx (range (- l) (+ r 1))]
#             [dy dx])
#        n (count ml)
#        [mtr mts] (utl/select (vec ml) [(- n 1) 1] rs)]
#    ;[(mapv (partial mlp.schemmlp/slide-history m) mtr)
#    [(mapv (partial mlp.schemmlp/slide-history m) (vec ml))
#     (mapv (partial mlp.schemmlp/slide-history m) mts)]))

#(defn meander-0-geometry-variation [size]
#  (for [g0 [2]
#        [g1 g3] (concat (for [g1 [ 2  3  4] g3 [ 2]] [g1 g3])
#                        (for [g1 [-2 -3 -4] g3 [-2]] [g1 g3]))
#        g2 [2 3 4] g4 [2] g5 [2]]
#    (mlp.meander/meander-0 size [(+ g0 g2) g1 g2 g3 g4 g5])))

#(defn ring-0-geometry-variation [size]
#  (for [g0 [4]
#        [g1 g2] (concat (for [g1 [ 4] g2 [ 2  3  4]] [g1 g2])
#                        (for [g1 [-4] g2 [-2 -3 -4]] [g1 g2]))
#        g3 [2 3 4] g4 [1] g5 [2]]
#    (mlp.meander/ring-0 size [g0 g1 g2 g3 g4 g5])))

#(defn ring-1-geometry-variation [size]
#  (for [g0 [2] g1 [1]
#        [g2 g3] (concat (for [g2 [ 2] g3 [ 2  3  4]] [g2 g3])
#                        (for [g2 [-2] g3 [-2 -3 -4]] [g2 g3]))
#        g4 [2 3 4] g5 [2]]
#    (mlp.meander/ring-1 size [g0 g1 g2 g3 g4 g5])))

#(defn test-pattern [size]
#  (as-> (concat ;(meander-0-geometry-variation size)
#                (ring-0-geometry-variation size)
#                (ring-1-geometry-variation size)) s
#        ; [h h ...]
#        (mapv (fn [geom]
#                (position-variation geom (utl/xorshift 2 4 6 8)))
#              s)
#        ; [ [[h h ...] [h h ...]]
#        ;   [[h h ...] [h h ...]]
#        ;   ... ]
#
#        (apply map vector s)
#        ; [ [[h h ...] [h h ...] ...]
#        ;   [[h h ...] [h h ...] ...] ]
#        ))

#(defn print-data [l k fname]
#  (with-open [o (clojure.java.io/writer fname)]
#    (binding [*out* o]
#      (doseq [x1 l]
#        (doseq [x (k x1)]
#          (print " " x))
#        (newline)))))

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
