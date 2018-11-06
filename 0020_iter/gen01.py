def gen01():
  i = 0
  while i < 5:
    yield i
    i += 1

g = gen01()
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
