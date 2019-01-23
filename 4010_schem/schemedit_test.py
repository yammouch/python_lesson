import schemedit as sce

if sce.surrounding(4, 6) == \
   [ [3, 6, 0, 3, 6, 0]
   , [4, 6, 0, 5, 6, 0]
   , [4, 5, 1, 4, 5, 1]
   , [4, 6, 1, 4, 7, 1] ]:
  print("[OK]", end="")
else:
  print("[ER]", end="")
print(" surrounding")

def radix(rdx, i):
  acc = []
  while 0 < i:
    acc.append(i % rdx)
    i = i // rdx
  return acc

def radix_inv(rdx, a):
  acc = 0
  for i in range(len(a)-1, -1, -1):
    acc = acc*rdx + a[i]
  return acc

def radix2_inv(a):
  return radix_inv(2, a)

def decode1(n, str):
  acc = []
  for c in str:
    i = 0 if c == ' ' else int(c, 16)
    a = radix(2, i) + [0] * n
    acc.append(a[0:n])
  return acc

def decode(n, strs):
  return [decode1(n, str) for str in strs]

def mapd(d, f, s):
  if d <= 0:
    return f(s)
  else:
    return [mapd(d-1, f, x) for x in s]

test_pattern = \
["    1     ", "          ",
 "    1     ", "          ",
 "  223222  ", "  222222  ",
 "    1     ", "          ",
 "    1     ", "          ",
 "    1     ", "          ",
 "  227222  ", "          ",
 "    1     ", "          ",
 "    1     ", "          ",
 "    1     ", "          "]
tested   = test_pattern[0::2]
expected = test_pattern[1::2]
val      = sce.trace(decode(3, tested), 2, 3, 1)
if val == decode(2, expected):
  print("[OK]", end="")
else:
  print("[ER]", end="")
print(" trace")

test_pattern =\
["          ",
 "  322272  ",
 "  1   1 1 ",
 "  1   1 1 ",
 "          ",
 "          "]
val = sce.beam(decode(3, test_pattern), [1, 4], 1)
if val == [[1, 2], [1, 6]]:
  print("[OK]", end="")
else:
  print("[ER]", end="")
print(" beam")
val = sce.beam(decode(3, test_pattern), [1, 2], 0)
if val == [[1, 2], [4, 2]]:
  print("[OK]", end="")
else:
  print("[ER]", end="")
print(" beam")

test_pattern = \
["          ", "          ",
 "  322272  ", "  322272  ",
 "  1   1 1 ", "  1   1 1 ",
 "  1   1 1 ", "  1   1 1 ",
 "          ", "          ",
 "  322272  ", "          ",
 "  1   1 1 ", "          ",
 "  1   1 1 ", "          ",
 "          ", "          "]
field  = decode(3, test_pattern[0::2])
traced = decode(3, test_pattern[1::2])
if sce.drawable(4, 2, 1, traced, field):
  print("[OK]", end="")
else:
  print("[ER]", end="")
print(' drawable')
if sce.drawable(6, 2, 1, traced, field):
  print("[OK]", end="")
else:
  print("[ER]", end="")
print(' drawable')
if not sce.drawable(5, 3, 1, traced, field):
  print("[OK]", end="")
else:
  print("[ER]", end="")
print(' drawable')

test_pattern = \
["          ", "          ", "          ",
 "          ", "          ", "          ",
 "  2223222 ", "  2227222 ", "  2227222 ",
 "     1    ", "     1    ", "     1    ",
 "   221    ", "   221    ", "   225    ",
 "     1    ", "     1    ", "     1    ",
 "  322322  ", "  322322  ", "  322322  ",
 "  1  1    ", "  1  1    ", "  1  1    ",
 "  222     ", "  222     ", "  222     ",
 "          ", "          ", "          "]
field, ex1, ex2 = [decode(3, test_pattern[i::3]) for i in range(3)]
if sce.add_dot([2, 2], 8, 1, field, field) == ex1:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' add_dot')
if sce.add_dot([2, 5], 8, 0, field, field) == ex2:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' add_dot')
if sce.add_dot([7, 2], 8, 1, field, field) == field:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' add_dot')

test_pattern = \
["          ", "          ", "          ",
 "          ", "  222222  ", "          ",
 "          ", "          ", "    1     ",
 "          ", "          ", "    1     ",
 "          ", "          ", "    1     ",
 "          ", "          ", "    1     ",
 "          ", "          ", "    1     ",
 "          ", "          ", "          ",
 "          ", "          ", "          ",
 "          ", "          ", "          "]
field, ex1, ex2 = [decode(3, test_pattern[i::3]) for i in range(3)]
if sce.draw_net_1([1, 2], 8, 1, field) == ex1:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' draw_net_1')
if sce.draw_net_1([2, 4], 7, 0, field) == ex2:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' draw_net_1')

test_pattern = \
["          ", "          ", "          ", "          ",
 "          ", "          ", "          ", "      1   ",
 "     222  ", "          ", "     222  ", "     232  ",
 "          ", "          ", "          ", "      1   ",
 "     222  ", "     222  ", "  222222  ", "     232  ",
 "          ", "          ", "          ", "      1   ",
 "     222  ", "     222  ", "     222  ", "     222  ",
 "          ", "          ", "          ", "          ",
 "          ", "          ", "          ", "          ",
 "          ", "          ", "          ", "          "]
field, traced, ex1, ex2 = [decode(3, test_pattern[i::4]) for i in range(4)]
#if sce.stumble([2, 2], 5, 1, traced, field)[1] == None:
if sce.stumble([2, 2], 5, 1, traced, field) == None:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' stumble')
if sce.stumble([4, 2], 6, 1, traced, field)[1] == ex1:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' stumble')
#if sce.stumble([1, 5], 6, 0, traced, field)[1] == None:
if sce.stumble([1, 5], 6, 0, traced, field) == None:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' stumble')
if sce.stumble([1, 6], 6, 0, traced, field)[1] == ex2:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' stumble')

test_pattern = \
["          ", "          ", "          ", "          ",
 "  1       ", "  1       ", "  1       ", "  1       ",
 "  1       ", "  1       ", "  1       ", "  1       ",
 "  1   22  ", "  1       ", "  1   22  ", "  1   22  ",
 "  1       ", "  1       ", "  1       ", "  1       ",
 "  1       ", "  1       ", "  1       ", "  1       ",
 "          ", "          ", "          ", "  1       ",
 "          ", "          ", "          ", "          ",
 "          ", "          ", "          ", "          ",
 "          ", "          ", "          ", "          "]
field, traced, ex1, ex2 = [decode(3, test_pattern[i::4]) for i in range(4)]
if sce.reach([3, 2], 'u', traced, field)[1] == ex1:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' reach')
if sce.reach([7, 2], 'u', traced, field)[1] == ex2:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' reach')
if sce.reach([3, 8], 'l', traced, field) == None:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' reach')
if sce.reach([3, 8], 'r', traced, field) == None:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' reach')

test_pattern = \
["          ", "          ", "          ", "          ",
 "  32221   ", "  1   1   ", "  3222    ", "  32221   ",
 "  1   1   ", "  1   1   ", "  1       ", "  1   1   ",
 "  1   1   ", "  1   1   ", "  1       ", "  1   1   ",
 "  72225   ", "  72225   ", "  72221   ", "  1   1   ",
 "  1   1   ", "  1   1   ", "  1   1   ", "  1   1   ",
 "      1   ", "      1   ", "      1   ", "      1   ",
 "      1   ", "      1   ", "      1   ", "      1   ",
 "    22    ", "    22    ", "    22    ", "    22    ",
 "          ", "          ", "          ", "          "]
field, ex1, ex2, ex3 = [decode(3, test_pattern[i::4]) for i in range(4)]
if sce.debridge([1, 2], 6, 1, field) == ex1:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' debridge')
if sce.debridge([1, 6], 4, 0, field) == ex2:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' debridge')
if sce.debridge([4, 2], 6, 1, field) == ex3:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' debridge')

test_pattern = \
["          ", "          ", "          ", "          ",
 "  1   1   ", "      1   ", "  1       ", "  1   1   ",
 "  1   1   ", "      1   ", "  1       ", "  1   1   ",
 "  1   1   ", "      1   ", "  1       ", "  1   1   ",
 "  72225   ", "  32225   ", "  72221   ", "  72225   ",
 "  1   1   ", "  1   1   ", "  1   1   ", "  1   1   ",
 "      1   ", "      1   ", "      1   ", "      1   ",
 "      1   ", "      1   ", "      1   ", "      1   ",
 "    22    ", "    22    ", "    22    ", "          ",
 "          ", "          ", "          ", "          "]
field, ex1, ex2, ex3 = [decode(3, test_pattern[i::4]) for i in range(4)]
if sce.shave([1, 2], 9, 'd', field) == ex1:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' shave')
if sce.shave([1, 6], 9, 'd', field) == ex2:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' shave')
if sce.shave([8, 4], 9, 'r', field) == ex3:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' shave')

test_pattern = \
["          ", "          ",
 "  32221   ", "      1   ",
 "  1   1   ", "      1   ",
 "  1   1   ", "      1   ",
 "  2222322 ", "      722 ",
 "      1   ", "      1   ",
 "      1   ", "      1   ",
 "      1   ", "      1   ",
 "          ", "          ",
 "          ", "          "]
field, ex1 = [decode(3, test_pattern[i::2]) for i in range(2)]
if sce.move_x(field, [2, 2], 6) == ex1:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' move_x')

test_pattern = \
["          ", "          ",
 "  32221   ", "          ",
 "  1   1   ", "          ",
 "  1   1   ", "          ",
 "  2222322 ", "  2222722 ",
 "      1   ", "      1   ",
 "      1   ", "      1   ",
 "      1   ", "      1   ",
 "          ", "          ",
 "          ", "          "]
field, ex1 = [decode(3, test_pattern[i::2]) for i in range(2)]
if sce.move_y(field, [1, 4], 4) == ex1:
  print('[OK]', end='')
else:
  print('[ER]', end='')
print(' move_y')
