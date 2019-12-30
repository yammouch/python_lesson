import collections

def origins(g):
  reached = {}
  for v in g:
    reached[v] = None

  for v in g:
    for v2 in g[v]:
      reached[v2] = 1

  return [v for v in reached if not reached[v]]

def dist(g):
  retval = {}
  for v in g:
    retval[v] = None

  q = collections.deque(origins(g))
  for x in q:
    retval[x] = 0

  while 0 < len(q):
    n0 = q.pop()
    for n1 in g[n0]:
      if retval[n1] == None or retval[n0] + 1 < retval[n1]:
        retval[n1] = retval[n0] + 1
        q.appendleft(n1)

  return retval

def htruck_range(us, ds):
  retval = {}
  for i, pair in enumerate(zip(us, ds)):
    for x in pair:
      if x in retval:
        retval[x][1] = i
      else:
        retval[x] = [i, None]
  if None in retval:
    del retval[None]
  return retval

def make_vconst(us, ds):
  retval = {}
  for u, d in zip(us, ds):
    if u in retval:
      retval[u].append(d)
    else:
      retval[u] = [d]
  if None in retval:
    del retval[None]
  return retval

def make_cols(us, ds):
  cols = [set() for _ in range(len(us))]
  hr = htruck_range(us, ds)
  for net in hr:
    for i in range(hr[net][0], hr[net][1]+1):
      cols[i].add(net)
  return cols

def make_zones(us, ds):
  acc = []
  maxset = set()
  for s in make_cols(us, ds):
    if maxset <= s:
      maxset = s
    elif not maxset >= s:
      acc.append(maxset)
      maxset = s
  acc.append(maxset)
  return acc

def main():
  g = { 'a': ['b', 'c']
      , 'b': ['c'     ]
      , 'c': [        ] }

  # ['a']
  print(origins(g))
  print(dist(g))
  ex1 = ([None, 1, 2, 3, 1], [3, 2, 1, 1, 3])
  #print(htruck_range([None, 1, 2, 3], [3, 2, None, 1]))
  print(htruck_range(*ex1))
  print(make_vconst(*ex1))
  print(make_cols(*ex1))
  print(make_zones(*ex1))

if __name__ == '__main__':
  main()
