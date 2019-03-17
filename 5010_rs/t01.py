import rs

for i in range(len(rs.p2b) // 0x10):
  print(' '.join('{:02X}'.format(x) for x in rs.p2b[i*0x10:(i+1)*0x10]))
print('')
for i in range(len(rs.p2b) // 0x10):
  print(' '.join('{:02X}'.format(x) for x in rs.b2p[i*0x10:(i+1)*0x10]))
print('')

enc = rs.encode([0, 1, 2])
print(' '.join(['{:02X}'.format(x) for x in enc]))

syn = rs.syndrome(enc)
print(' '.join(['{:02X}'.format(x) for x in syn]))

enc[0] = 1
syn = rs.syndrome(enc)
print(' '.join(['{:02X}'.format(x) for x in syn]))
