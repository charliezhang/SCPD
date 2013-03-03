
import random
f = open("features.small.txt", "w")
f2 = open("targets.small.txt", "w")
for x in xrange(0, 100):
  f.write(",".join([str(random.random()/2) for y in xrange(0, 20)]) + "\n")
  f2.write("1\n")
for x in xrange(0, 100):
  f.write(",".join([str(random.random()/2+0.5) for y in xrange(0, 20)]) + "\n")
  f2.write("-1\n")
