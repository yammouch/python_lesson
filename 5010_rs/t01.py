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

enc[1] = 0
syn = rs.syndrome(enc)
print(' '.join(['{:02X}'.format(x) for x in syn]))

# 00:01 FF:00 FF:00 / EB:30 E7:03 -> 14:0D -> 00:01 FB:17
#       FB:17 FF:00               -> 10:F3 -> FB:17 F7:64
#             F7:64
qp, r = rs.euc([0x00] + [0xFF] * 2, syn)
qp_d = qp[0:-1]
for i in range(len(qp_d)//2): 
  qp_d[-i*2] = 0xFF
print(' '.join(['{:02X}'.format(x) for x in qp  ]))
print(' '.join(['{:02X}'.format(x) for x in r   ]))
print(' '.join(['{:02X}'.format(x) for x in qp_d]))

pos = [rs.assign(qp,   (0xFF-x)%0xFF) for x in range(len(enc))]
val = [rs.assign(qp_d, (0xFF-x)%0xFF) for x in range(len(enc))]
print(' '.join(['{:02X}'.format(x) for x in pos]))
print(' '.join(['{:02X}'.format(x) for x in val]))

