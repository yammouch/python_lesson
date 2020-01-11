import s0010 as dut
import sys
import xml.etree.ElementTree as ET

def make_tr(row):
  pxg = 13
  pad = pxg
  tr = ET.Element('tr')
  for cell in row:
    td = ET.Element('td')
    td.append(dut.nets_to_svg(pxg, pad, cell))
    tr.append(td)
  return tr

def body():
  table = ET.Element('table', {'border': '1'})

  tr = \
  [ [ [1, [0, 2], [4   ] ]
    , [2, [1   ], [2, 3] ] ] ]

  table.append(make_tr(tr))

  return table

def main():
  progname = '.'.join(sys.argv[0].split('.')[:-1])
  t = ET.Element('html')
  h = ET.SubElement(t, 'head', attrib={'a': '1'}, text='hoge')
  title = ET.Element('title')
  title.text = progname
  h.append(title)
  b = ET.SubElement(t, 'body')
  b.append(body())

  ET.ElementTree(t).write('{}.html'.format(progname), method='html')

if __name__ == '__main__':
  main()
