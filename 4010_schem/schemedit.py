import copy
import numpy as np

def format_field(ar):
  acc = np.zeros(ar.shape[1:])
  for i in range(ar.shape[0]):
    acc += ar[i] * 2**i
  sacc = []
  for i in range(ar.shape[1]):
    line = ''.join(['  ' if x == 0 else '{:02X}'.format(int(x))
                    for x in acc[i]])
    sacc.append(line)
  return sacc

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

def stumble(from_p, to, o, traced, field):
  if all(drawable(y, x, o, traced, field) for y, x in range_p(from_p, to, o)):
    return [draw_net_1(from_p, to, o, traced),
            add_dot(from_p, to, o, traced,
                    draw_net_1(from_p, to, o, field))]

def prog(d, p):
  retval = copy.copy(p)
  if d == 'u':
    retval[0] -= 1
  elif d == 'd':
    retval[0] += 1
  elif d == 'l':
    retval[1] -= 1
  elif d == 'r':
    retval[1] += 1
  return retval

def search_short(from_p, d, traced, field):
  cy = len(field   ) - 1
  cx = len(field[0]) - 1
  dops, to = ['d',  0] if d == 'u' else \
             ['u', cy] if d == 'd' else \
             ['r',  0] if d == 'l' else \
             ['l', cx] if d == 'r' else None
  for x in range_p(from_p, to, d):
    if [x1 for x1 in d_match(x, [1, 1], traced, field) if not x1 == dops]:
      return range_p(from_p, x, d)

def reach(from_p, d, traced, field):
  ps = search_short(from_p, d, traced, field)
  o = 0 if d in {'u', 'd'} else \
      1 if d in {'l', 'r'} else None
  if ps and all([drawable(y, x, o, traced, field) for y, x in ps]):
    to = ps[-1]
    drawn = draw_net_1(from_p, to[o], o, field)
    traced_new = draw_net_1(from_p, to[o], o, traced)
    if len(d_match(to, [1, 1], traced_new, drawn)) == 3:
      drawn[to[0]][to[1]][2] = 1
    return [traced_new, drawn]

def debridge(from_p, to, o, field):
  fld = copy.deepcopy(field)
  for y, x in range_n(from_p, to, o):
    fld[y][x][o] = 0
  for y, x in range_p(from_p, to, o):
    dm = len(d_match([y, x], [1], fld))
    if dm in [0, 1, 2]:
      fld[y][x][2] = 0
    elif dm == 3:
      fld[y][x][2] = 1
  return fld

def shave(from_p, to, d, field):
  #print('### shave ###')
  o = 0 if d in ['u', 'd'] else \
      1 if d in ['l', 'r'] else None
  p = from_p
  fld = copy.deepcopy(field)
  dirs = ['u', 'd', 'l', 'r', 'f'] if d == 'u' else \
         ['d', 'u', 'l', 'r', 'f'] if d == 'd' else \
         ['l', 'r', 'u', 'd', 'f'] if d == 'l' else \
         ['r', 'l', 'u', 'd', 'f'] if d == 'r' else None
  while True:
    n = []
    for x in dirs:
      n.extend(net(p[0], p[1], x, fld))
    if (n == [1, 0, 0, 0, 0] or n == [1, 0, 1, 1, 0]) and \
       all([e == 0 for e in fld[p[0]][p[1]][3:]]) and \
       not (p[o] == to):
      fld[p[0]-1 if d == 'u' else p[0]][p[1]-1 if d == 'l' else p[1]][o] = 0
      p = prog(d, p)
    else:
      n_net = len([x for x in n[0:4] if x == 1])
      if n_net in [0, 1, 2]:
        fld[p[0]][p[1]][2] = 0
      if n_net == 3:
        fld[p[0]][p[1]][2] = 1
      return fld

def move_element(field, from_p, d, to):
  to_p = copy.copy(from_p)
  to_p[d] = to
  from_el = field[from_p[0]][from_p[1]][3:]
  to_el   = field[to_p  [0]][to_p  [1]][3:]
  if all([x == 0 for x in to_el]):
    fld = copy.deepcopy(field)
    fld[to_p  [0]][to_p  [1]][3:] = from_el
    fld[from_p[0]][from_p[1]][3:] = [0] * (len(fld[0][0]) - 3)
    return fld

def move_x(field, from_p, to):
  y, x = from_p
  [y0, _], [y1, _] = beam(field, from_p, 0)
  traced = trace(field, y, x, 0)
  d, dop = ('r', 'l') if x < to else ('l', 'r')
  fld = move_element(field, from_p, 1, to)
  fld = reach([y0, to], dop, traced, fld)
  fld = reach([y1, to], dop, *fld) if fld else None
  fld = stumble([y0, to], y1, 0, *fld) if fld else None
  fld = debridge([y0, x], y1, 0, fld[1]) if fld else None
  fld = shave([y0, x], to, d, fld) if fld else None
  fld = shave([y1, x], to, d, fld) if fld else None
  return fld

def move_y(field, from_p, to):
  y, x = from_p
  [_, x0], [_, x1] = beam(field, from_p, 1)
  traced = trace(field, y, x, 1)
  d, dop = ('d', 'u') if y < to else ('u', 'd')
  fld = move_element(field, from_p, 0, to)
  fld = reach([to, x0], dop, traced, fld)
  fld = reach([to, x1], dop, *fld) if fld else None
  fld = stumble([to, x0], x1, 1, *fld) if fld else None
  fld = debridge([y, x0], x1, 1, fld[1]) if fld else None
  #for row in fld: print(row)
  #for row in format_field(np.moveaxis(np.array(fld), 2, 0)): print(row)
  #for row in fld[1]: print([radix_inv(2, x) for x in row])
  #print(fld)
  #print(type(fld))
  #print('T' if fld else 'F')
  fld = shave([y, x0], to, d, fld) if fld else None
  #fld = shave([y, x0], to, d, fld) if fld != None else None
  fld = shave([y, x1], to, d, fld) if fld else None
  #fld = shave([y, x1], to, d, fld) if fld != None else None
  return fld

def count_corner_cross(field):
  cy = len(field)
  cx = len(field[0])
  retval = 0
  for y in range(cy):
    for x in range(cx):
      a = []
      for d in 'udlr':
        a.extend(net(y, x, d, field))
      if (a[0] or a[1]) and (a[2] or a[3]):
        retval += 1
  return retval
