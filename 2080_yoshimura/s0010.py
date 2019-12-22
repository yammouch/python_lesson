import sys
import xml.etree.ElementTree as ET

def net(pxg, pad, n, lo):
  xs = n[1] + n[2]
  d = ' '.join \
  ( ['M {} {} L {} {} Z'.format \
     ( pad + x*pxg, pad +        0
     , pad + x*pxg, pad + n[0]*pxg )
     for x in n[1] ]
  + ['M {} {} L {} {} Z'.format \
     ( pad + x*pxg, pad +   lo*pxg
     , pad + x*pxg, pad + n[0]*pxg )
     for x in n[2] ]
  + ['M {} {} L {} {} Z'.format \
     ( pad + min(xs)*pxg, pad + n[0]*pxg
     , pad + max(xs)*pxg, pad + n[0]*pxg ) ] )
  e = ET.Element('path',
   {'d': d, 'stroke': 'black', 'stroke-width': '2', 'fill': 'transparent',
    'stroke-linejoin': 'round'})
  return e

def nets_to_svg(pxg, pad, nets):
  print(nets)
  size = [ max(n[0] for n in nets) + 1
         , max(max(n[1] + n[2]) for n in nets) ]
  s = ET.Element('svg',
   {'width' : str(pad*2 + size[1]*pxg),
    'height': str(pad*2 + size[0]*pxg) })
  for n in nets:
    s.append(net(pxg, pad, n, size[1]-1))
  return s

def make_tr(row):
  pxg = 13
  pad = pxg
  tr = ET.Element('tr')
  for cell in row:
    td = ET.Element('td')
    td.append(nets_to_svg(pxg, pad, cell))
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
