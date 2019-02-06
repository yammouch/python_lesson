import schemedit as sce

def radix2(length, n):
  retval = []
  for i in range(length):
    retval.append(n & 1)
    n >>= 1
  return retval

schem = \
[ '  ,  ,  ,  ,  ,  ,  ,  ,  ,  ' ,
  '0A,02,02,02,  ,  ,  ,  ,  ,  ' ,
  '  ,  ,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,  ,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,  ,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,  ,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,03,02,02,03,02,20,  ,02,10' ,
  '  ,01,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,01,  ,  ,01,  ,  ,  ,  ,  ' ,
  '  ,02,02,02,  ,  ,  ,  ,  ,  ' ]

class MyEnv():

  def __init__(self):
    retval = reset(self):
    return retval

  def reset(self):
    self.state = \
    [ [radix2(6, int('0' + cell, 16)) for cell in row.split(',')]
      for row in schem ]
    return np.moveaxis(np.array(self.state), 2, 0)

  def step(self, action):
    reward = 0
    ### 'reward' is to be programmed.
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
      self.state = sce.move_x(self.state, cmd[2:0:-1], cmd[0])
    elif action == 0: # move-y
      done = False:
      if command[2] <= command[0]:
        command[0] += 1
      self.state = sce.move_y(self.state, cmd[2:0:-1], cmd[0])
    return np.moveaxis(np.array(self.state), 2, 0), reward, done, None
