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

