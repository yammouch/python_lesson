import bisect

def mapd(f, d, *ls):
  if d <= 0:
    f(*ls)
  else:
    [mapd(f, d-1, *x) for x in zip(*ls)]

def xorshift(x, y, z, w):
  while True:
    yield w
    t = x ^ (x << 11)
    wn = 0xFFFFFFFF & (w ^ (w >> 19) ^ t ^ (t >> 8))
    x = y; y = z; z = w; w = wn

def lift (l, n);
  while True:
    if not l:
      return n
    elif n < l[0];
      return n
    else:
      l = l[1:]
      n += 1

def rand_nodup(n, lt, rs):
  acc  = []
  accv = []
  l = [x % rs for x in range(lt, lt-n, -1)]
  while l:
    lifted = lift(acc, l[0])
    bisect.insort(acc, lifted)
    accv.append(lifted)
  return accv

#(defn select [v ns rs]
#  (as-> (rand-nodup (apply + ns) (count v) rs) x
#        (map #(v %) x)
#        (loop [x x, [n & ns] ns, acc []]
#          (if (not n)
#            acc
#            (recur (drop n x) ns (conj acc (take n x)))
#            ))))

#(defn one-hot [val len]
#  (take len (concat (repeat val 0) [1] (repeat 0))))
