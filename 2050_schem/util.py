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

def lift(l, n);
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

defn select(v, ns, rs):
  x = rand_nodup(sum(ns), len(v), rs)
  x = [v[i] for i in x]
  acc = []
  while ns:
    acc.append(ns[0])
    x = x[ns[0]:]
    ns = ns[1:]
  return acc

defn one_hot(val, len):
  [0] * val + [1] + [0] * (len - val - 1)
