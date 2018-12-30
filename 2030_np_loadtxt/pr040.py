import numpy as np

def format_field(ar):
  acc = np.zeros(ar.shape[1:])
  for i in range(ar.shape[0]):
    acc += ar[i] * 2**i
  sacc = []
  for i in range(ar.shape[1]):
    line = ','.join(['  ' if x == 0 else '{:02X}'.format(int(x))
                    for x in acc[i]])
    sacc.append(line)
  return sacc

a = np.loadtxt("../../jocl_lesson/0270_sasimi/train_in.dat", dtype=np.float32)
print(a.shape)
b = np.moveaxis(a.reshape(-1, 10, 10, 6), 3, 1)
print(b.shape)

#print(a[0, ..., ..., ...].shape)
#print(a[0, :, :, :].shape)
print(type(b[0]))
print((b[0]).shape)
print((b[0]).shape[0])
for line in format_field(b[0]):
  print(line)
