class C01:
  def __init__(self):
    print("C01.__init__")
    self.x = 1

class C02:
  def __init__(self):
    print("C02.__init__")
    self.x = 2

def retobj(t):
  return t()

for i in (C01, C02):
  o = retobj(i)
  print(o.x)
