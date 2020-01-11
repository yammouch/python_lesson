import sys
import xml.etree.ElementTree as ET

def net(pxg, pad, n, lo, ofs=(0, 0), transpose=False):
  xs = n[1] + n[2]
  ofs_x = ofs[1]*pxg + pad
  ofs_y = ofs[0]*pxg + pad
  format_string = \
   'M {1} {0} L {3} {2} Z' if transpose else \
   'M {0} {1} L {2} {3} Z'
  d = ' '.join \
  ( [format_string.format \
     ( ofs_x + x*pxg, ofs_y +        0
     , ofs_x + x*pxg, ofs_y + n[0]*pxg )
     for x in n[1] ]
  + [format_string.format \
     ( ofs_x + x*pxg, ofs_y +   lo*pxg
     , ofs_x + x*pxg, ofs_y + n[0]*pxg )
     for x in n[2] ]
  + [format_string.format \
     ( ofs_x + min(xs)*pxg, ofs_y + n[0]*pxg
     , ofs_x + max(xs)*pxg, ofs_y + n[0]*pxg ) ] )
  e = ET.Element('path',
   {'d': d, 'stroke': 'black', 'stroke-width': '2', 'fill': 'transparent',
    'stroke-linejoin': 'round'})
  return e

def nets_to_svg(pxg, pad, nets, ofs=(0, 0), transpose=False):
  size = [ max(n[0] for n in nets) + 1
         , max(max(n[1] + n[2]) for n in nets) ]
  # width and height should be specified outside of this function.
  if transpose:
    s = ET.Element('svg',
     {'width' : str(pad*2 + (size[0]+ofs[0])*pxg),
      'height': str(pad*2 + (size[1]+ofs[1])*pxg) })
  else:
    s = ET.Element('svg',
     {'width' : str(pad*2 + (size[1]+ofs[1])*pxg),
      'height': str(pad*2 + (size[0]+ofs[0])*pxg) })
  for n in nets:
    s.append(net(pxg, pad, n, size[0], ofs=ofs, transpose=transpose))
  return s

def gates_to_nets(gates1, gates2):
  grid_per_lgrid = 4
  retval = {}
  for i, g in enumerate(gates1):
    if g[0] == 'and':
      if g[3] not in retval:
        retval[g[3]] = [[], []]
      retval[g[3]][0].append(i*grid_per_lgrid+2)
    elif g[0] == 'not':
      if g[2] not in retval:
        retval[g[2]] = [[], []]
      retval[g[2]][0].append(i*grid_per_lgrid+2)
  for i, g in enumerate(gates2):
    if g[0] == 'and':
      if g[1] not in retval:
        retval[g[1]] = [[], []]
      if g[2] not in retval:
        retval[g[2]] = [[], []]
      retval[g[1]][1].append(i*grid_per_lgrid+1)
      retval[g[2]][1].append(i*grid_per_lgrid+3)
    elif g[0] == 'not':
      if g[1] not in retval:
        retval[g[1]] = [[], []]
      retval[g[1]][1].append(i*grid_per_lgrid+2)
    elif g[0] == 'out':
      if g[1] not in retval:
        retval[g[1]] = [[], []]
      retval[g[1]][1].append(i*grid_per_lgrid+2)
  return [[i+1] + retval[x] for i, x in enumerate(retval)]

def gate2_to_svg(pxg, pad, gates1, gates2, ofs=(0, 0)):
  return nets_to_svg \
  ( pxg, pad, gates_to_nets(gates1, gates2)
  , ofs=(0, 0), transpose=True )
