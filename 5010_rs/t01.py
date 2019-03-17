import rs

enc = rs.encode([0, 1, 2])
print(' '.join(['{:02X}'.format(x) for x in enc]))

syn = rs.syndrome(enc)
print(' '.join(['{:02X}'.format(x) for x in syn]))

enc[0] = 1
syn = rs.syndrome(enc)
print(' '.join(['{:02X}'.format(x) for x in syn]))
