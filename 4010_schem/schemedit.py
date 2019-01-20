import copy

def radix_inv(rdx, a):
  acc = 0
  for i in range(len(a)-1, -1, -1):
    acc = acc*rdx + a[i]
  return acc

def radix2_inv(a):
  return radix_inv(2, a)

def mapd(d, f, s):
  if d <= 0:
    return f(s)
  else:
    return [mapd(d-1, f, x) for x in s]

def surrounding(y,  x):
  return [ [y-1, x  , 0, y-1, x  , 0]   # up
         , [y  , x  , 0, y+1, x  , 0]   # down
         , [y  , x-1, 1, y  , x-1, 1]   # left
         , [y  , x  , 1, y  , x+1, 1] ] # right

def net(y, x, d, *fields):
  idx = [y-1, x   , 0] if d == 'u' else \
        [y  , x   , 0] if d == 'd' else \
        [y  , x-1 , 1] if d == 'l' else \
        [y  , x   , 1] if d == 'r' else \
        [y  , x   , 2] if d == 'f' else None
  acc = []
  for fld in fields:
    try:
      n = fld[idx[0]][idx[1]][idx[2]]
    except IndexError:
      n = 0
    acc.append(n)
  return acc

def d_match(p, v, *fields):
  return [d for d in ['u', 'd', 'l', 'r'] if net(p[0], p[1], d, *fields) == v]

def range_2d(end, from_p, to, o):
  o = 0 if o in {'u', 'd', 0} else \
      1 if o in {'l', 'r', 1} else None
  q = from_p[o]
  if isinstance(to, list): to = to[o]
  r = range(*([q + end - 1, to - 1, -1] if to < q else [q, to + end]))
  if o == 0:
    return [[y, from_p[1]] for y in r]
  elif o == 1:
    return [[from_p[0], x] for x in r]

def range_p(from_p, to, o):
  return range_2d(1, from_p, to, o)
def range_n(from_p, to, o):
  return range_2d(0, from_p, to, o)

def trace_search_dir(field, traced, y, x, d):
  search = [s for s in surrounding(y, x) if field[s[0]][s[1]][s[2]] == 1]
  n_surrounding_nets = len([s for s in search if field[s[0]][s[1]][s[2]] == 1])
  if not (field[y][x][2] == 1 or
          n_surrounding_nets <= 2): # surrounded by 0, 1, 2 nets
    search = [s for s in search if s[2] == d]
  search = [s for s in search if traced[s[0]][s[1]][s[2]] == 0]
  return search

def trace(field, y, x, d):
  cy = len(field)
  cx = len(field[0])
  stack = [[y, x, d]]
  traced = [[[0 for i in range(2)] for i in range(cx)] for i in range(cy)]
  while stack:
    py, px, pd = stack[-1]
    search = trace_search_dir(field, traced, py, px, pd)
    stack = stack[0:-1]
    for s in search:
      sy, sx, sd = s[3:]
      if -1 < sy < cy and -1 < sx < cx:
        stack.append(s[3:])
      traced[s[0]][s[1]][s[2]] = 1
  return traced

def beam(field, p, o):
  if o == 0:
    u = p[0]
    while not (net(u, p[1], 'u', field) == [0] or
               net(u, p[1], 'f', field) == [1]):
      u -= 1
    d = p[0]
    while not (net(d, p[1], 'd', field) == [0] or
               net(d, p[1], 'f', field) == [1]):
      d += 1
    return [[u, p[1]], [d, p[1]]]
  elif o == 1:
    l = p[1]
    while not (net(p[0], l, 'l', field) == [0] or
               net(p[0], l, 'f', field) == [1]):
      l -= 1
    r = p[1]
    while not (net(p[0], r, 'r', field) == [0] or
               net(p[0], r, 'f', field) == [1]):
      r += 1
    return [[p[0], l], [p[0], r]]

def drawable(y, x, os, traced, field): # os:  orientation straight
  dir = ['d', 'u', 'r', 'l'] if os == 0 else \
        ['r', 'l', 'd', 'u'] if os == 1 else None
  sfwd, sbwd, ofwd, obwd = [net(y, x, d, field, traced) for d in dir]
  return False if  sfwd        ==  [1, 0]          else \
         False if  sbwd        ==  [1, 0]          else \
         True  if [obwd, ofwd] == [[1, 0], [1, 0]] else \
         False if  ofwd        ==  [1, 0]          else \
         False if  obwd        ==  [1, 0]          else \
         True

def add_dot(from_p, to, os, traced, field):
  retval = copy.deepcopy(field)
  for y, x in [p for p in range_p(from_p, to, os)
               if len(d_match(p, [1, 1], field, traced)) == 3]:
    retval[y][x][2] = 1
  return retval

def draw_net_1(from_p, to, o, field):
  retval = copy.deepcopy(field)
  for y, x in range_n(from_p, to, o):
    retval[y][x][o] = 1
  return retval

#(defn stumble [from to o traced field]
#  (when (every? (fn [[y x]] (drawable? y x o traced field))
#                (range-p from to o))
#    [(draw-net-1 from to o traced)
#     (as-> field fld
#           (draw-net-1 from to o fld)
#           (add-dot from to o traced fld))]))

#(defn prog [d p]
#  (let [[o f] (case d :u [0 dec] :d [0 inc] :l [1 dec] :r [1 inc])]
#    (update-in p [o] f)))

#(defn search-short [from d traced field]
#  (let [cy (- (count field) 1) cx (- (count (first field)) 1)
#        [dops to] (case d :u [:d 0] :d [:u cy] :l [:r 0], :r [:l cx])]
#    (let [[p] (filter #(as-> % x
#                             (d-match x [1 1] traced field)
#                             (remove #{dops} x)
#                             (not (empty? x)))
#                      (range-p from to d))]
#      (if p (range-p from p d))
#      )))

#(defn reach [[y x :as from] d traced field]
#  (let [ps (search-short from d traced field)
#        o (case d (:u :d) 0 (:l :r) 1)]
#    (if (and ps
#             (every? (fn [[y x]] (drawable? y x o traced field))
#                     ps))
#      (let [to (last ps)
#            drawn (draw-net-1 from (to o) o field)
#            traced-new (draw-net-1 from (to o) o traced)]
#        [traced-new
#         (if (as-> (d-match to [1 1] traced-new drawn) x
#                   (count x)
#                   (= 3 x))
#           (assoc-in drawn (conj to 2) 1)
#           drawn)]))))

#(defn debridge [from to o field]
#  (as-> field fld
#        (reduce #(assoc-in %1 (conj %2 o) 0)
#                fld (range-n from to o))
#        (reduce #(case (count (d-match %2 [1] %1))
#                   (0 1 2) (assoc-in %1 (conj %2 2) 0)
#                   3       (assoc-in %1 (conj %2 2) 1)
#                   %1)
#                fld (range-p from to o))))

#(defn shave [from to d field]
#  (let [o (case d (:u :d) 0 (:l :r) 1)]
#    (loop [[y x :as p] from fld field]
#      (let [n (mapcat #(net y x % fld)
#                      (case d
#                        :u [:u :d :l :r :f]
#                        :d [:d :u :l :r :f]
#                        :l [:l :r :u :d :f]
#                        :r [:r :l :u :d :f]))]
#        (if (and (or (= n [1 0 0 0 0])
#                     (= n [1 0 1 1 0]))
#                 (every? zero? (drop 3 (get-in fld p)))
#                 (not= (p o) to))
#          (recur (prog d p)
#                 (assoc-in fld
#                  [(if (= d :u) (- y 1) y)
#                   (if (= d :l) (- x 1) x)
#                   (case d (:u :d) 0 (:l :r) 1)]
#                  0))
#          (case (->> (take 4 n)
#                     (filter (partial = 1))
#                     count)
#            (0 1 2) (assoc-in fld [y x 2] 0)
#            3       (assoc-in fld [y x 2] 1)
#            4       fld))))))

#(defn move-element [field [y x :as from] d to]
#  (let [to (assoc from d to)
#        from-el (drop 3 (get-in field from))
#        to-el   (drop 3 (get-in field to  ))]
#    (if (every? zero? to-el)
#      (as-> field fld
#            (update-in fld to
#             (fn [v] (vec (concat (take 3 v) from-el))))
#            (update-in fld from
#             (fn [v] (vec (take (count v)
#                                (concat (take 3 v) (repeat 0))
#                                ))))))))

#(defn move-x [field [y x :as from] to]
#  (let [[[y0 _] [y1 _]] (beam field from 0)
#        traced (trace field y x 0)
#        [d dop] (if (< x to) [:r :l] [:l :r])]
#    (as-> field fld
#          (move-element fld from 1 to)
#          (reach [y0 to] dop traced fld)
#          (if (nth fld 1) (apply reach [y1 to] dop fld))
#          (if (nth fld 1) (apply stumble [y0 to] y1 0 fld))
#          (if (nth fld 1) (debridge [y0 x] y1 0 (nth fld 1)))
#          (if fld (shave [y0 x] to d fld))
#          (if fld (shave [y1 x] to d fld)))))

#(defn move-y [field [y x :as from] to]
#  (let [[[_ x0] [_ x1]] (beam field from 1)
#        traced (trace field y x 1)
#        [d dop] (if (< y to) [:d :u] [:u :d])]
#    (as-> field fld
#          (move-element fld from 0 to)
#          (reach [to x0] dop traced fld)
#          (if (nth fld 1) (apply reach [to x1] dop fld))
#          (if (nth fld 1) (apply stumble [to x0] x1 1 fld))
#          (if (nth fld 1) (debridge [y x0] x1 1 (nth fld 1)))
#          (if fld (shave [y x0] to d fld))
#          (if fld (shave [y x1] to d fld))
#          )))
