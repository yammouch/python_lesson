import matplotlib.pyplot as plt

def main():
  atama = 500e4
  permonth = 10e4
  value_init = 3000e4
  value_min = 500e4
  interest = 2.5 # unit : %
  pay_year = 200e4

  price   = [ [ 0, value_init         ] ]
  balance = [ [ 0, value_init - atama ] ]
  paid    = [ [ 0, atama              ] ]

  i = 1
  while 0 < balance[-1][1] and i <= 50:
    price.append(
     [ i
     , value_min if price[-1][1] <= value_min + pay_year else
       price[-1][1] - pay_year ] )
    balance.append(
     [ i
     , 0 if balance[-1][1] <= pay_year else
       balance[-1][1] - pay_year ] )
    balance.append(
     [ i
     , 0 if balance[-1][1] == 0 else
       balance[-1][1] * (1 + 0.01*interest) ] )
    paid.append([i, paid[-1][1] + pay_year])
    i += 1

  print(price)
  print([x[0] for x in price])

  for curve in [price, balance, paid]:
    plt.plot([x[0] for x in curve], [x[1] for x in curve])

  plt.show()

main()
