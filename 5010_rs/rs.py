p2b = [0] * 0x100
p2b[-1] = 0
p2b[0] = 0x01
for i in range(0xFE):
  shifted = (p2b[i] << 1) & 0xFF
  p2b[i+1] = shifted ^ 0x71 if p2b[i] & (1 << 7) else shifted

b2p = [0] * 0x100
b2p[0] = 0xFF
for i in range(0xFF):
  b2p[p2b[i]] = i

def addc(x1, x2):
  return b2p[p2b[x1] ^ p2b[x2]]

def mulc(x1, x2):
  if 0xFF <= x1 or 0xFF <= x2:
    return 0xFF
  else:
    return (x1 + x2) % 0xFF

def divc(n, d):
  if 0xFF <= d:
    raise ValueError()
  else:
    return (n - d) % 0xFF

def divp_inplace(n, d):
  for i in range(len(n)-len(d)+1):
    n[i] = divc(n[i], d[0])
    for j in range(1, len(d)):
      n[i+j] = addc(n[i+j], mulc(d[j], n[i]))
    #print(' '.join('{:02X}'.format(x) for x in n))

def remp(n, d):
  a = n[:]
  divp_inplace(a, d)
  i = len(n) - len(d) + 1
  while i < len(a) and a[i] == 0xFF:
    i += 1
  return a[i:]

def divp(n, d):
  a = n[:]
  divp_inplace(a, d)
  i = len(n) - len(d) + 1
  while i < len(a) and a[i] == 0xFF:
    i += 1
  return a[0:len(n) - len(d) + 1], a[i:]

def assign(p, x):
  acc = 0xFF
  for c in p:
    acc = addc(mulc(x, acc), c)
  return acc

# (x + 1)(x + a)
# = x^2 + (a + 1)x + a
def encode(l):
  a = l[:] + [0xFF] * 2
  divp_inplace(a, [b2p[x] for x in [0x01, 0x03, 0x02]])
  return l[:] + a[-2:]

def syndrome(l):
  return [assign(l, x) for x in range(1, -1, -1)]

def addp(p1, p2):
  retval = None; l = None; s = None
  if len(p1) < len(p2): l = p2; s = p1
  else:                 l = p1; s = p2
  retval = l[:]
  for i in range(len(s)):
    retval[-1-i] = addc(retval[-1-i], s[-1-i])
  return retval

def mulp(p1, p2):
  retval = [0xFF] * (len(p1) + len(p2) - 1)
  for i in range(len(p1)):
    for j in range(len(p2)):
      retval[i+j] = addc(retval[i+j], mulc(p1[i], p2[j]))
  return retval

# [m0 m1] [ 0 1 ]
# [m2 m3] [ 1 q ]
def euc(p1, p2):
  m = [[], [], [], []]
  while 1 < len(p2):
    q, r = divp(p1, p2)
    m = [ m[1]                      , 
          addp(m[0], mulp(m[1], q)) ,
          m[3]                      ,
          addp(m[2], mulp(m[3], q)) ]
    print('[p1]: ' + ' '.join('{:02X}'.format(x) for x in p1))
    print('[p2]: ' + ' '.join('{:02X}'.format(x) for x in p2))
    print('[q ]: ' + ' '.join('{:02X}'.format(x) for x in q ))
    print('[r ]: ' + ' '.join('{:02X}'.format(x) for x in r ))
    print('[m ]: ' + ','.join(' '.join('{:02X}'.format(x) for x in p) for p in m))
    p1 = p2; p2 = r
  return m[3], r
