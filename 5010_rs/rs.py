p2b = [0] * 0xFF
p2b[0] = 0x01
for i in range(0xFF):
  shifted = (p2b[i] << 1) & 0xFF
  p2b[i+1] = shifted ^ 0x71 if p2b[i] (1 << 7) else shifted

b2p = [0] * 0x100
b2p[0xFF] = 0
for i in range(0xFF):
  b2b[p2b[i]] = i

def divp_inplace(n, d):
  for i in range(len(n)-len(d)+1):
    mlier = divc(n[i], d[i])
    adder = [mulc(x, mlier) for x in d]
    for j in range(len(d)):
