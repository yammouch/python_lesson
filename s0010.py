import sys
import xml.etree.ElementTree as ET

def net(pxg, n, lo):
  ['M {} {} L {} {} Z'.format(x*pxg,    0, x*pxg, n[0]*pxg) for x in n[1]]
  ['M {} {} L {} {} Z'.format(x*pxg, x*lo, x*pxg, n[0]*pxg) for x in n[1]]
  n[1] + n[2]

def inport(pxg, y, x):
  ps = [
   [y       , x           ],
   [y-pxg//4, x-   pxg//4 ],
   [y-pxg//4, x-3*(pxg//4)],
   [y+pxg//4, x-3*(pxg//4)],
   [y+pxg//4, x-   pxg//4 ] ]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps) + ' Z'
  e = ET.Element('path',
   {'d': d, 'stroke': 'black', 'stroke-width': '2', 'fill': 'transparent',
    'stroke-linejoin': 'round'})
  return e

def outport(pxg, y, x):
  ps = [
   [y       , x+3*(pxg//4)],
   [y-pxg//4, x+2*(pxg//4)],
   [y-pxg//4, x           ],
   [y+pxg//4, x           ],
   [y+pxg//4, x+2*(pxg//4)] ]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps) + ' Z'
  e = ET.Element('path',
   {'d': d, 'stroke': 'black', 'stroke-width': '2', 'fill': 'transparent',
    'stroke-linejoin': 'round'})
  return e

def fanout_dot(pxg, y, x):
  return ET.Element('circle',
   {'cx': str(x), 'cy': str(y), 'r': str(pxg//3), 'fill': 'black',
    'stroke-width': '0'})

def inverter(pxg, y, x):
  r = pxg//4
  ps = [
   [y - 3*(pxg//4), x              ],
   [y + 3*(pxg//4), x              ],
   [y             , x + 2*pxg - 2*r] ]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps) + ' Z'
  tri = ET.Element('path',
   {'d': d, 'stroke': 'black', 'stroke-width': '2', 'fill': 'transparent',
    'stroke-linejoin': 'round'})
  cir = ET.Element('circle',
   {'cx': str(x + 2*pxg - r), 'cy': str(y), 'r': str(r),
    'stroke': 'black', 'stroke-width': '2', 'fill': 'transparent'})
  return [tri, cir]

def vline(pxg, y, x):
  ps = [
   [y    , x],
   [y+pxg, x]]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps)
  e = ET.Element('path',
   {'d': d, 'stroke': 'black', 'stroke-width': '2', 'stroke-linecap': 'round'})
  return e

def hline(pxg, y, x):
  ps = [
   [y, x    ],
   [y, x+pxg]]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps)
  e = ET.Element('path',
   {'d': d, 'stroke': 'black', 'stroke-width': '2', 'stroke-linecap': 'round'})
  return e

def filled_square(pxg, y, x):
  r = pxg//3
  ps = [
   [y-r, x-r],
   [y-r, x+r],
   [y+r, x+r],
   [y+r, x-r] ]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps) + ' Z'
  e = ET.Element('path',
   {'d': d, 'stroke-width': '0', 'fill': '#3399FF'})
  return e

def varrow(pxg, y, x, to):
  retval = []
  if y < to:
    ps = [
     [y        , x],
     [to-pxg//4, x] ]
  else:
    ps = [
     [y        , x],
     [to+pxg//4, x] ]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps) + ' Z'
  e = ET.Element('path',
   {'d': d, 'stroke': '#3399FF', 'stroke-width': '4', 'fill': 'transparent',
    'stroke-linecap': 'round'})
  retval.append(e)

  if y < to:
    ps = [
     [to           , x       ],
     [to-2*(pxg//3), x-pxg//2],
     [to-2*(pxg//3), x+pxg//2] ]
  else:
    ps = [
     [to           , x       ],
     [to+2*(pxg//3), x-pxg//2],
     [to+2*(pxg//3), x+pxg//2] ]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps) + ' Z'
  e = ET.Element('path',
   {'d': d, 'stroke-width': '0', 'fill': '#3399FF'})
  retval.append(e)

  return retval

def harrow(pxg, y, x, to):
  retval = []
  if x < to:
    ps = [
     [y, x        ],
     [y, to-pxg//4] ]
  else:
    ps = [
     [y, x        ],
     [y, to+pxg//4] ]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps) + ' Z'
  e = ET.Element('path',
   {'d': d, 'stroke': '#3399FF', 'stroke-width': '4', 'fill': 'transparent',
    'stroke-linecap': 'round'})
  retval.append(e)

  if x < to:
    ps = [
     [y       , to           ],
     [y-pxg//2, to-2*(pxg//3)],
     [y+pxg//2, to-2*(pxg//3)] ]
  else:
    ps = [
     [y       , to           ],
     [y-pxg//2, to+2*(pxg//3)],
     [y+pxg//2, to+2*(pxg//3)] ]
  d = 'M ' + ' L '.join('{} {}'.format(p[1], p[0]) for p in ps) + ' Z'
  e = ET.Element('path',
   {'d': d, 'stroke-width': '0', 'fill': '#3399FF'})
  retval.append(e)

  return retval

def cell_to_element(cell, pxg, pad, y, x):
  retval = []
  if cell[0]:
    retval.append(vline(pxg, pad+y*pxg, pad+x*pxg))
  if cell[1]:
    retval.append(hline(pxg, pad+y*pxg, pad+x*pxg))
  if cell[2]:
    retval.append(fanout_dot(pxg, pad+y*pxg, pad+x*pxg))
  if cell[3]:
    retval.append(inport(pxg, pad+y*pxg, pad+x*pxg))
  if cell[4]:
    retval.append(outport(pxg, pad+y*pxg, pad+x*pxg))
  if cell[5]:
    retval.extend(inverter(pxg, pad+y*pxg, pad+x*pxg))
  return retval

def field_to_elements(field, pxg, pad):
  size = [len(field), len(field[0])]
  retval = []
  for y, x in ((y, x) for y in range(size[0]) for x in range(size[1])):
    retval.extend(cell_to_element(field[y][x], pxg, pad, y, x))
  return retval

def cmd_to_elements(cmd, pxg, pad):
  org = [pad + x*pxg for x in cmd['org']]
  to = pad + cmd['dst']*pxg
  retval = [filled_square(pxg, org[0], org[1])]
  if cmd['cmd'] == 'move-y':
    retval.extend(varrow(pxg, org[0], org[1], to))
  if cmd['cmd'] == 'move-x':
    retval.extend(harrow(pxg, org[0], org[1], to))
  return retval

def pair_to_svg(pair, pxg, pad):
  size = [len(pair['field']), len(pair['field'][0])]
  s = ET.Element('svg',
   {'width' : str(pad*2 + (size[1] - 1)*pxg),
    'height': str(pad*2 + (size[0] - 1)*pxg) })
  for e in cmd_to_elements(pair['cmd'], pxg, pad):
    s.append(e)
  for e in grid(pxg, pad, size):
    s.append(e)
  for e in field_to_elements(pair['field'], pxg, pad):
    s.append(e)
  return s

def history_to_tr(hist):
  pxg = 13
  pad = pxg
  tr = ET.Element('tr')
  for pair in hist:
    td = ET.Element('td')
    td.append(pair_to_svg(pair, pxg, pad))
    tr.append(td)
  return tr

def body():
  table = ET.Element('table', {'border': '1'})

  for h in histories:
    table.append(history_to_tr(h))

  for h in meander.position_variation(histories[0], itertools.count(0))[0]:
    table.append(history_to_tr(h))

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
