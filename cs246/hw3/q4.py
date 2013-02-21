from collections import defaultdict
import copy
import itertools
from optparse import OptionParser
import random
import sets
import sys
import time

def preprocess(graph_file):
  f = open(graph_file)
  V = sets.Set()
  num_edge = 0
  for line in f:
    a, b = line.strip().split('\t')
    if a not in V:
      V.add(a)
    if b not in V:
      V.add(b)
    num_edge += 1
  f.close()
  return V, num_edge

def count_edge(graph_file, S):
  f = open(graph_file)
  count = 0
  for line in f:
    a, b = line.strip().split('\t')
    if (a in S) and (b in S):
      count += 1
  f.close()
  return count

def find_dense(graph_file, eps, removed=None):
  V, e = preprocess(graph_file)
  if removed:
    V.difference_update(removed)
    if len(V) == 0:
      return None, None, None, None, None
  S_bar = copy.copy(V)
  rho_S_bar = float(e) / len(V)
  S = copy.copy(V)
  num_iter = 0
  list_rho = []
  list_num_edge = []
  list_size_s = []
  while len(S) > 0:
    num_iter += 1
    deg = defaultdict(int)
    num_edge = 0
    f = open(graph_file)
    for line in f:
      a, b = line.strip().split('\t')
      if removed and ((a in removed) or (b in removed)):
        continue
      if (a not in S) or (b not in S):
        continue
      deg[a] += 1  
      deg[b] += 1
      num_edge += 1
    f.close()
    rho_S = float(num_edge) / len(S)
    list_rho.append(rho_S)
    list_num_edge.append(num_edge)
    list_size_s.append(len(S))
    A = sets.Set()
    num_edge_remove = 0
    for v in S:
      if deg[v] <= 2 * (1 + eps) * rho_S:
        A.add(v)
        num_edge_remove += deg[v]
    num_edge_remove /= 2
    S.difference_update(A)
    if len(S) == 0:
      break
    rho_S = float(num_edge - num_edge_remove) / len(S)
    if rho_S > rho_S_bar:
      rho_S_bar = rho_S
      S_bar = copy.copy(S)
  return S_bar, num_iter, list_rho, list_num_edge, list_size_s

def main():
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="file", type="string",
                    help="File containing the graph.")
  (options, args) = parser.parse_args()

  for eps in [0.05, 0.1, 0.5, 1, 2]:
    S_bar, num_iter, list_rho, list_num_edge, list_size_s = find_dense(options.file, eps)
    print "Eps: %f, num iteration: %d" % (eps, num_iter)
    print list_rho
    print list_num_edge
    print list_size_s

  removed = sets.Set()
  eps = 0.05
  list_rho = []
  list_num_edge = []
  list_size_s = []
  for j in xrange(1, 21):
    print "%d-th iter" % j
    S_bar, t1, t2, t3, t4 = find_dense(options.file, eps, removed)
    if not S_bar:
      print "Remaining graph is empty"
      break
    num_edge = count_edge(options.file, S_bar)
    print "rho: %f" % (float(num_edge) / len(S_bar))
    list_rho.append(float(num_edge) / len(S_bar))
    print "num_edge: %d" % num_edge
    list_num_edge.append(num_edge)
    print "size_S_bar: %d" % len(S_bar)
    list_size_s.append(len(S_bar))
    removed = removed.union(S_bar)
    print S_bar
  print list_rho
  print list_num_edge
  print list_size_s

if __name__ == '__main__':
  main()

