import s0010 as dut
import sys
import xml.etree.ElementTree as ET
import yaml

def make_tr0(row):
  pxg = 13
  pad = pxg
  tr = ET.Element('tr')
  for cell in row:
    td = ET.Element('td')
    td.append(dut.nets_to_svg(pxg, pad, cell, ofs=(1, 2), transpose=True))
    tr.append(td)
    td = ET.Element('td')
    td.append(dut.nets_to_svg(pxg, pad, cell, transpose=True))
    tr.append(td)
    td = ET.Element('td')
    td.append(dut.nets_to_svg(pxg, pad, cell))
    tr.append(td)
  return tr

def make_tr1(ed):
  pxg = 13
  pad = pxg
  tr = ET.Element('tr')
  td = ET.Element('td')
  td.append(dut.gate2_to_svg(pxg, pad, ed[0], ed[1]))
  tr.append(td)
  return tr

def body(ed):
  table = ET.Element('table', {'border': '1'})

  tr = \
  [ [ [1, [0, 2], [4   ] ]
    , [2, [1   ], [2, 3] ] ] ]

  table.append(make_tr1(ed))
  table.append(make_tr0(tr))

  return table

def main():
  progname = '.'.join(sys.argv[0].split('.')[:-1])
  with open('s0010.yml') as f:
    ed = yaml.load(f)
  print(dut.gates_to_nets(ed[0], ed[1]))

  t = ET.Element('html')
  h = ET.SubElement(t, 'head', attrib={'a': '1'}, text='hoge')
  title = ET.Element('title')
  title.text = progname
  h.append(title)
  b = ET.SubElement(t, 'body')
  b.append(body(ed))

  ET.ElementTree(t).write('{}.html'.format(progname), method='html')


if __name__ == '__main__':
  main()
