import matplotlib.pyplot as plt

def main():
  atama = 500e4
  permonth = 10e4
  price = 3000e4
  interest = 2.5 # unit : %

  price_curve = []
  price_curve.append([0, price])

  for i in range(1, 30):
    price_curve.append(
     [i, 500e4 if price_curve[-1][1] <= 700e4 else price_curve[-1][1] - 200e4])


  print(price_curve)
  print([x[0] for x in price_curve])

  plt.plot([x[0] for x in price_curve], [x[1] for x in price_curve])
  plt.show()

  #paid = []

main()
