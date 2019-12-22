def origins(vs, es):
  reached = {}
  for v in vs:
    reached[v] = None

  for v in vs:
    for v2 in es[v]:
      reached[v2] = 1

  return [v for v in reached if not reached[v]]

def main():
  # ['a']
  print origins( ['a', 'b', 'c']
               , { 'a': ['b', 'c']
                 , 'b': ['c'     ]
                 , 'c': [        ] } )

if __name__ == '__main__':
  main()
