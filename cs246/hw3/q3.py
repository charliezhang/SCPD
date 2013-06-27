import math
from collections import defaultdict

_O = {
  1: [2, 3, 5],
  2: [2, 4],
  3: [1]
}
_I = {
  1: [3],
  2: [1, 2],
  3: [1],
  4: [2],
  5: [1]
}
C1 = 0.8
C2 = 0.8

def update(sa, sb, O, I):
  sa2 = defaultdict(float)
  sb2 = defaultdict(float)
  na = len(O)
  nb = len(I)
  for x in range(1, na + 1):
    for y in range(x, na + 1):
      if x == y:
        sa2[(x, y)] = 1
        continue
      for i in O[x]:
        for j in O[y]:
          if i > j: k = (j, i)
          else: k = (i, j)
          sa2[(x, y)] += sb[k]
      N = len(O[x]) * len(O[y])
      sa2[(x, y)] *= (1 - math.pow(1 - C1, N)) / N
      #sa2[(x, y)] *= C1 / N
  for x in range(1, nb + 1):
    for y in range(x, nb + 1):
      if x == y:
        sb2[(x, y)] = 1
        continue
      for i in I[x]:
        for j in I[y]:
          if i > j: k = (j, i)
          else: k = (i, j)
          sb2[(x, y)] += sa[k]
      N = len(I[x]) * len(I[y])
      sb2[(x, y)] *= (1 - math.pow(1 - C2, N)) / N
      #sb2[(x, y)] *= C2 / N
  return sa2, sb2

def build_complete_graph(a, b):
  O = defaultdict(list)
  I = defaultdict(list)
  for i in range(1, a + 1):
    for j in range(1, b + 1):
      O[i].append(j)
      I[j].append(i)
  return O, I

def compute_sim(O, I, iter):
  sa = defaultdict(float)
  sb = defaultdict(float)
  for i in range(1, len(O) + 1):
    sa[(i, i)] = 1
  for i in range(1, len(I) + 1):
    sb[(i, i)] = 1
  for i in range(0, iter):
#    print "Round %d:\\\\ " % (i + 1)
    sa, sb = update(sa, sb, O, I)
#    print "$s_A$:\\\\"
#    for k, v in sa.items(): print "%s: %f \\\\" % (k, v)
#    print "$s_B$:\\\\"
#    for k, v in sb.items(): print "%s: %f \\\\" % (k, v)
  return sa, sb

def main():
  print compute_sim(_O, _I, 3)
  K21 = build_complete_graph(2, 1)
  print compute_sim(K21[0], K21[1], 300)
  K22 = build_complete_graph(2, 2)
  print compute_sim(K22[0], K22[1], 300)

if __name__ == '__main__':
  main()
