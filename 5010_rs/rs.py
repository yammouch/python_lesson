p2b = [0] * 0x100
p2b[-1] = 0
p2b[0] = 0x01
for i in range(0xFE):
  shifted = (p2b[i] << 1) & 0xFF
  p2b[i+1] = shifted ^ 0x71 if p2b[i] & (1 << 7) else shifted

b2p = [0] * 0x100
b2p[0xFF] = 0
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
    n[i] = divc(n[i], d[i])
    for j in range(1, len(d)):
      n[i+j] = addc(n[i+j], mulc(d[j], n[i]))

def assign(p, x):
  acc = 0xFF
  for c in p:
    acc = addc(mulc(x, acc), c)
  return acc

# (x + 1)(x + a)
# = x^2 + (a + 1)x + a
def encode(l):
  a = l + [0xFF] * 2
  divp_inplace(a, [b2p[x] for x in [0x01, 0x03, 0x02]])
  return a

def syndrome(l):
  return [assign(l, x) for x in range(1, -1, -1)]
