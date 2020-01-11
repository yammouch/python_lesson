import sys
import xml.etree.ElementTree as ET

def net(pxg, pad, n, lo, transpose=False):
  xs = n[1] + n[2]
  format_string = \
   'M {1} {0} L {3} {2} Z' if transpose else \
   'M {0} {1} L {2} {3} Z'
  d = ' '.join \
  ( [format_string.format \
     ( pad + x*pxg, pad +        0
     , pad + x*pxg, pad + n[0]*pxg )
     for x in n[1] ]
  + [format_string.format \
     ( pad + x*pxg, pad +   lo*pxg
     , pad + x*pxg, pad + n[0]*pxg )
     for x in n[2] ]
  + [format_string.format \
     ( pad + min(xs)*pxg, pad + n[0]*pxg
     , pad + max(xs)*pxg, pad + n[0]*pxg ) ] )
  e = ET.Element('path',
   {'d': d, 'stroke': 'black', 'stroke-width': '2', 'fill': 'transparent',
    'stroke-linejoin': 'round'})
  return e

def nets_to_svg(pxg, pad, nets, transpose=False):
  size = [ max(n[0] for n in nets) + 1
         , max(max(n[1] + n[2]) for n in nets) ]
  s = ET.Element('svg',
   {'width' : str(pad*2 + size[0 if transpose else 1]*pxg),
    'height': str(pad*2 + size[1 if transpose else 0]*pxg) })
  for n in nets:
    s.append(net(pxg, pad, n, size[1]-1, transpose=transpose))
  return s

