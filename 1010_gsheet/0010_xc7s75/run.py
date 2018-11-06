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
  return [row_dict[m[1]], int(m[2])-1, is_reserved(cells), cells[1]]

def read_file():
  f = open('xc7s75fgga676pkg.txt', 'r')
  str = f.read()
  lines = str.splitlines()
  while not lines[0].startswith('Pin'):
    lines = lines[1:]
  lines = lines[1:677]
  parsed = [parse_line(l) for l in lines]
  return parsed

def make_req(cells):
  return {
    'updateCells': {
      'rows': {
        'values': {
          'userEnteredFormat': {
            'backgroundColor': {
              'red'  : 0,
              'green': 0,
              'blue' : 0,
              'alpha': 0
            }
          }
        }
      },
      'fields': '*',
      'range': {
        'sheetId'          : 0,
        'startRowIndex'    : cells[0],
        'endRowIndex'      : cells[0]+1,
        'startColumnIndex' : cells[1],
        'endColumnIndex'   : cells[1]+1
      }  
    }
  }

def main():
  table = read_file()
  requests = [make_req(x) for x in table if x[2]]
  for i in range(3):
    print(requests[i])

main()
