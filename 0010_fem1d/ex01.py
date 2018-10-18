import numpy as np
import numpy.linalg as LA

pos = np.linspace(0, 1, 5)
lns = pos[1:] - pos[:-1]

n, = pos.shape
m = np.zeros([n, n])
d = np.zeros([n, n])

for i in range(n-1):
  d[i  , i  ] += 1.0/lns[i]
  d[i  , i+1] -= 1.0/lns[i]
  d[i+1, i  ] -= 1.0/lns[i]
  d[i+1, i+1] += 1.0/lns[i]
  m[i  , i  ] += lns[i]/3.0
  m[i  , i+1] += lns[i]/6.0
  m[i+1, i  ] += lns[i]/6.0
  m[i+1, i+1] += lns[i]/3.0

#print(d)
#print(m)
e, v = LA.eig(np.dot(LA.inv(m), d))
print(e)
print(v)

