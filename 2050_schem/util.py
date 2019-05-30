import bisect
from functools import reduce

def mapd(f, d, *ls):
  if d <= 0:
    return f(*ls)
  else:
    return [mapd(f, d-1, *x) for x in zip(*ls)]

def xorshift(x, y, z, w):
  while True:
    yield w
    t = x ^ (x << 11)
    wn = 0xFFFFFFFF & (w ^ (w >> 19) ^ t ^ (t >> 8))
    x = y; y = z; z = w; w = wn

def lift(l, n):
  while True:
    if not l:
      return n
    elif n < l[0]:
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

def select(v, ns, rs):
  x = rand_nodup(sum(ns), len(v), rs)
  x = [v[i] for i in x]
  acc = []
  while ns:
    acc.append(ns[0])
    x = x[ns[0]:]
    ns = ns[1:]
  return acc

def one_hot(val, len):
  [0] * val + [1] + [0] * (len - val - 1)

def parse_cell(cell):
  a = []
  try:
    n = int(cell, 16)
  except ValueError:
    return [0] * 6
  for _ in range(6):
    a.append(n % 2)
    n = n // 2
  return a

def parse_row(s):
  return [parse_cell(c) for c in s.split(',')]

def format_row(row):
  r = []
  for c in row:
    c = reduce(lambda acc, x: acc*2+x, c[::-1])
    c = '  ' if c == 0 else '{:02X}'.format(c)
    r.append(c)
  return ','.join(r)

def format_field(field):
  return "\n".join(format_row(r) for r in field)
