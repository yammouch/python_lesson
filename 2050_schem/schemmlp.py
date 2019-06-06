import util as utl
import schemprep as smp

def mlp_input_cmd(cmd, size):
  y, x = cmd['org']
  dst = cmd['dst']
  cy, cx = size
  cmd = cmd['cmd']
  return ([1, 0] if cmd == 'move-y' else [0, 1]) + \
         utl.one_hot(y, cy) + \
         utl.one_hot(x, cx) + \
         utl.one_hot(dst, max(cy, cx))

def slide_pair(p, mv):
  y, x = p['cmd']['org']
  cmd = p['cmd']
  return {'field': smp.slide(p['field'], mv),
          'cmd': {'cmd': cmd['cmd'],
                  'org': [y + mv[0], x + mv[1]],
                  'dst': cmd['dst'] + mv[0 if cmd == 'move-y' else 1]}}

def slide_history(h, mv):
  return [slide_pair(p, mv) for p in h]
