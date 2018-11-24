import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def main():
  atama      = 500e4
  value_init = 3000e4
  value_min  = 0
  interest   = 1.3 # unit : %
  pay_year   = 120e4
  sell_cost  = 100e4

  value   = [ [ 0, value_init         ] ]
  balance = [ [ 0, value_init - atama ] ]
  paid    = [ [ 0, atama              ] ]
  rent    = [                           ]

  i = 1
  while 0 < balance[-1][1] and i <= 50:
    value.append(
     [ i
     , value_min if value[-1][1] <= value_min + pay_year else
       value[-1][1] - pay_year ] )
    balance.append(
     [ i
     , 0 if balance[-1][1] <= pay_year else
       balance[-1][1] - pay_year ] )
    balance.append(
     [ i
     , 0 if balance[-1][1] == 0 else
       balance[-1][1] * (1 + 0.01*interest) ] )
    paid.append([i, paid[-1][1] + pay_year])
    rent.append(
     [ i
     ,   (paid[-1][1] - value[-1][1] + balance[-1][1] + sell_cost)
       / (i * 12) ] )
    i += 1

  for curve in [value, balance, paid]:
    plt.plot([x[0] for x in curve], [x[1] / 100e4 for x in curve])
  for curve in [rent]:
    plt.plot([x[0] for x in curve], [x[1] /   1e4 for x in curve])
  #plt.xaxis.set_minor_locator(MultipleLocator(5))
  #plt.yaxis.set_minor_locator(MultipleLocator(5))
  #plt.locator_params(nbins=4)
  plt.minorticks_on()
  plt.grid(which='major', color='black', linestyle='-')
  plt.grid(which='minor', color='black', linestyle='--')

  plt.show()

main()
