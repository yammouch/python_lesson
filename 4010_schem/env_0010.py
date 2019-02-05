import schemedit as sce

class MyEnv():

  def __init__(self):
    self.state = 0
    self.success_cnt = 0

  def reset(self):
    self.state = 0
    return np.array([self.state, self.state ^ 1])

  def step(self, action):
    if action == self.state:
      reward = 1
      self.success_cnt += 1
    else:
      reward = 0
    self.state = self.state ^ 1
    #return [self.state, self.state ^ 1], reward, self.success_cnt >= 5, None
    return np.array([self.state, self.state ^ 1]), reward, False, None
