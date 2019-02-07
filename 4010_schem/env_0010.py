import schemedit as sce

def radix2(length, n):
  retval = []
  for i in range(length):
    retval.append(n & 1)
    n >>= 1
  return retval

schem = \
[ '                    ' ,
  '0A020202            ' ,
  '        01          ' ,
  '        01          ' ,
  '        01          ' ,
  '        01          ' ,
  '  030202030220  0210' ,
  '  01    01          ' ,
  '  01    01          ' ,
  '  020202            ' ]

class MyEnv():

  def __init__(self):
    retval = reset(self):
    return retval

  def reset(self):
    self.state = \
    [ [radix2(6, int('0' + row[i*2:(i+1)*2], 16)) for i in range(10)]
      for row in schem ]
    self.n_corner_cross = sce.count_corner_cross(self.state)
    return np.moveaxis(np.array(self.state), 2, 0)

  def step(self, action):
    command = []
    command.append(action % 9)
    action //= 9
    command.append(action % 10)
    action //= 10
    command.append(action % 10)
    action //= 10
    if action == 2:
      done = True:
    elif action == 1: # move_x
      done = False:
      if command[1] <= command[0]:
        command[0] += 1
      new_state = sce.move_x(self.state, cmd[2:0:-1], cmd[0])
    elif action == 0: # move-y
      done = False:
      if command[2] <= command[0]:
        command[0] += 1
      new_state = sce.move_y(self.state, cmd[2:0:-1], cmd[0])
    old_n_corner_cross = self.n_corner_cross
    if new_state:
      self.state = new_state
      self.n_corner_cross = sce.count_corner_cross(self.state)
    reward = 1 if self.n_corner_cross < old_n_corner_cross else 0
    return np.moveaxis(np.array(self.state), 2, 0), reward, done, None
