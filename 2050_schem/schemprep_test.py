import schemprep as dut

def parse_cell(cell):
  a = []
  try:
    n = int(cell, 16)
  except ValueError:
    return [0] * 6
  for _ in range(6):
    a.append(n % 2)
    n = n // 2
  return a

def parse_line(s):
  return [parse_cell(c) for c in s.split(',')]

fld = \
[parse_line(l) for l in
 ["0A,02,02,02,01,  ,  ,  ,  ,  ,  ,  ,  ,  ", # 0
  "  ,  ,  ,  ,01,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,  ,  ,01,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,03,02,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,01,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,02,02,02,20,  ,02,02,02,10,  ,  ,  ", # 5
  "  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ", # 10
  "  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ",
  "  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  ,  "]]
if dut.room(fld) == [0, 8, 0, 3]:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' room')

pattern = \
["..........", "..........", "..........", "..........", "..........",
 "..........", "..........", "..........", "....221...", "..........",
 "..........", "..........", "..........", "......1...", "..........",
 "....221...", ".221......", "......221.", "......1...", "..........",
 "......1...", "...1......", "........1.", "..........", "....221...",
 "......1...", "...1......", "........1.", "..........", "......1...",
 "..........", "..........", "..........", "..........", "......1...",
 "..........", "..........", "..........", "..........", ".........."]
pattern = [[parse_cell(c) for c in l] for l in pattern]
fld, ex1, ex2, ex3, ex4 = [pattern[i::5] for i in range(5)]
if dut.slide_1d(fld, -3, 1) == ex1:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' slide_1d')
if dut.slide_1d(fld, 2, 1) == ex2:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' slide_1d')
if dut.slide_1d(fld, -2, 0) == ex3:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' slide_1d')
if dut.slide_1d(fld, 1, 0) == ex4:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' slide_1d')
