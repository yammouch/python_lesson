import re

re_pin_pos = re.compile('([A-Z]+)([0-9]+)')
row_names = 'A B C D E F G H J K L M N P R T U V W Y AA AB AC AD AE AF'.split()
row_dict = {}
for i in range(len(row_names)):
  row_dict[row_names[i]] = i;

def is_reserved(cells):
  return cells[1].startswith('VCC') or cells[3] == 'NA' or cells[3] == '0'

def parse_line(str):
  cells = str.split()
  m = re_pin_pos.match(cells[0])
  ret = []
  ret.append(row_dict[m[1]])
  ret.append(int(m[2])-1)
  ret.append(cells[1])
  ret.append(is_reserved(cells))
  return ret

def read_file():
  f = open('xc7s75fgga676pkg.txt', 'r')
  str = f.read()
  lines = str.splitlines()
  while not lines[0].startswith('Pin'):
    lines = lines[1:]
  lines = lines[1:677]
  parsed = [parse_line(l) for l in lines]
  return parsed

def main():
  r = read_file()
  for i in range(50):
    print(r[i])

main()
