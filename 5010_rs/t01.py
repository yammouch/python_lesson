import rs

for i in range(len(rs.p2b) // 0x10):
  print(' '.join('{:02X}'.format(x) for x in rs.p2b[i*0x10:(i+1)*0x10]))
print('')
for i in range(len(rs.p2b) // 0x10):
  print(' '.join('{:02X}'.format(x) for x in rs.b2p[i*0x10:(i+1)*0x10]))
print('')

enc = rs.encode([0, 1, 2])
print(' '.join(['{:02X}'.format(x) for x in enc]))
print(' '.join(['{:02X}'.format(x) for x in rs.remp([0, 1, 2, 0xFF, 0xFF], [0x00, 0xE7, 0x01])]))

syn = rs.syndrome(enc)
print(' '.join(['{:02X}'.format(x) for x in syn]))

enc[0] = 1
syn = rs.syndrome(enc)
print(' '.join(['{:02X}'.format(x) for x in syn]))

qp, r = rs.euc([0x00] + [0xFF] * 2, syn)
print(' '.join(['{:02X}'.format(x) for x in qp]))
print(' '.join(['{:02X}'.format(x) for x in r ]))

pos = [rs.assign(qp, x) for x in range(len(enc))]
print(' '.join(['{:02X}'.format(x) for x in pos]))
