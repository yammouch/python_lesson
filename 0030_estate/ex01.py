import matplotlib.pyplot as plt

def main():
  atama = 500e4
  permonth = 10e4
  value_init = 3000e4
  value_min = 500e4
  interest = 2.5 # unit : %
  pay_year = 200e4

  price   = [ [0, value_init         ] ]
  balance = [ [0, value_init - atama ] ]

  for i in range(1, 30):
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

  print(price)
  print([x[0] for x in price])

  plt.plot([x[0] for x in price  ], [x[1] for x in price  ])
  plt.plot([x[0] for x in balance], [x[1] for x in balance])
  plt.show()

  #paid = []

main()
