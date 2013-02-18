from collections import defaultdict
import itertools
from optparse import OptionParser
import random
import sys

BETA = 0.8
N = 100

def load_graph(file):
  G = defaultdict(list)
  f = open(file)
  for line in f:
    parts = filter(bool, line.strip().split(' '))
    s = int(parts[0])
    e = int(parts[1])
    G[s].append(e)
  return G

def power_iter(G, iter):
  r = defaultdict(float)
  for i in xrange(1, N + 1):
    r[i] = 1 / N

  for i in xrange(0, iter):
    r_new = defaultdict(float)
    for s, dests in G.items():
      deg = len(dests)
      for dest in dests:
        r_new[dest] += r[s] / deg
    for k, v in r_new.items():
      r_new[k] = v * BETA + (1 - BETA) / 100
    r = r_new
  return r

def mc(G, R):
  r = defaultdict(float)

  for j in xrange(0, R):
    for i in xrange(1, N + 1):
      c = i
      while True:
        r[c] += 1
        if random.random() < (1 - BETA):
          break
        c = random.choice(G[c])
  for k, v in r.items():
    r[k] = v * (1 - BETA) / N / R
  return r

def errors(r_true, r, K):
  sum = 0
  errs = []
  sorted_r = sorted(r.items(), key=lambda x: -x[1])
  print sorted_r
  for k in xrange(1, K + 1):
    k, v = sorted_r[k - 1]
    sum += abs(r_true[k] - v)
    errs.append(sum / k)
  return errs

def main():
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="file", type="string",
                    help="Input file containing user browing history.")
  (options, args) = parser.parse_args()

  G = load_graph(options.file) 
  
  r = power_iter(G, 40)

  r2 = mc(G, 1)
  print r2

  errs = errors(r, r2, 100)
  print errs

if __name__ == '__main__':
  main()
