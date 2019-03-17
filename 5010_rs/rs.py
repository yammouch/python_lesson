p2b = [0] * 0xFF
p2b[0] = 0x01
for i in range(0xFF):
  shifted = (p2b[i] << 1) & 0xFF
  p2b[i+1] = shifted ^ 0x71 if p2b[i] (1 << 7) else shifted

b2p = [0] * 0x100
b2p[0xFF] = 0
for i in range(0xFF):
  b2b[p2b[i]] = i

def addc(x1, x2):
  return b2b[p2b[x1] ^ p2b[x2]]

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
    q = divc(n[i], d[i])
    for j in range(1, len(d)):
      n[i+j] = addc(n[i+j], mulc(d[i+j], q))
