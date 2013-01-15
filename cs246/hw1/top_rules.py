from collections import defaultdict
import itertools
from optparse import OptionParser
import sys

'''
Reads items and put in baskets.
Returns an array where the elements are arrays of items.
'''
def read(fname):
  f = open(fname)
  baskets = []
  for line in f:
    baskets.append(sorted(line.strip().split(" ")))
  return baskets

'''
Validate an itemset could be a frequent item set by
checking the frequency of subsets.
'''
def validate(freq, itemset, thres):
  size = len(itemset)
  if size == 1: return True
  for subset in itertools.combinations(itemset, size - 1):
    if not freq[size - 1].has_key(subset) or freq[size - 1][subset] < thres:
      return False
  return True

'''
Generates all frequent itemsets.
Also returns the map of supports, keyed by the set of items.
@param max_size The maximum size of set of items.
@param thres The minumum support to be considered frequent.
'''
def gen_frequent_itemsets(baskets, max_size, thres):
  freq = {}
  for size in xrange(1, max_size + 1):
    freq[size] = defaultdict(int)
    for basket in baskets:
      for itemset in itertools.combinations(basket, size):
        if validate(freq, itemset, thres):
          freq[size][itemset] += 1
    for k, v in freq[size].items():
      if v < thres:
        freq[size].pop(k)

  n_baskets = len(baskets)
  supports = {}
  for size in xrange(1, max_size + 1):
    for k, v in freq[size].items():
      supports[k] = float(v) / n_baskets

  return freq, supports

'''
Generate top {num_rules} rules from all itemsets in {itemsets}
given the scoring function defined by {func}.
'''
def print_rules(itemsets, supports, num_rules, func, sym, output):
  rules = []
  rules_set = {}
  for itemset in itemsets:
    for b in itertools.combinations(itemset, 1):
      a = tuple(item for item in itemset if item not in b)
      if sym and rules_set.has_key((b, a)): continue
      rules_set[(a, b)] = 1
      rules.append(((a, b), func(a, b, itemset, supports)))
  rules = sorted(rules, key=lambda x: -x[1])
  print 'Top %d rules by "%s" score:'\
      % ( num_rules, func.__name__)
  if output: f = open(output, "a")
  for ((a, b), score) in rules[0:num_rules]:
    out_str = "%s ==> %s, %f" % (a, b, score)
    if output: f.write(out_str + "\n")
    else: print out_str
  f.close()

'''
Scoring functions.
Caller must ensure that the support values of {a}, {b} and {a_and_b}
are defined in {S}
'''
def conf(a, b, a_and_b, S):
  return S[a_and_b] / S[a]

def lift(a, b, a_and_b, S):
  return conf(a, b, a_and_b, S) / S[b]

def conv(a, b, a_and_b, S):
  # Adding 1e-9 to avoid deviding by 0.
  return (1.0 - S[b]) / (1.0 + 1e-9 - conf(a, b, a_and_b, S))

def main():
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="fname", type="string",
                    help="Input file containing user browing history.")
  parser.add_option("-t", "--threshold", dest="thres", default=100, type="int",
                    help="Suppport threshold")
  parser.add_option("-s", "--size", dest="size", default=3, type="int",
                    help="Max num of items in itemset.")
  parser.add_option("-r", "--rules", dest="num_rules", default=5, type="int",
                    help="Num of rules to print.")
  parser.add_option("-o", "--output", dest="output", default="", type="string",
                    help="File to save all the rules.")
  (options, args) = parser.parse_args()

  if not options.fname:
    print "See usage: %s -h" % __file__
    return

  baskets = read(options.fname)
  itemsets, supports = gen_frequent_itemsets(
    baskets, options.size, options.thres)
  for func, sym in ((conf, False), (lift, True), (conv, False)):
    for size in xrange(2, options.size + 1):
      print_rules(itemsets[size], supports, options.num_rules, func, sym, options.output)

if __name__ == '__main__':
  main()
