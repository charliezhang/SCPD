import operator
u = [1, 0.25, 0, 0, 0.5, 0] 
v = [0.75, 0, 0, 0.2, 0.4, 0] 
w = [0, 0.1, 0.75, 0, 0, 1]
r = [[1, -1, 1, -1, 1, -1],
     [-1, -1, 1, 1, -1, 1],
     [1, 1, 1, 1, 1, 1]]
u3 = [ sum(map(operator.mul, u, r[i])) for i in (0,1,2)]
v3 = [ sum(map(operator.mul, v, r[i])) for i in (0,1,2)]
w3 = [ sum(map(operator.mul, w, r[i])) for i in (0,1,2)]
print u3
print v3
print w3

import math
# (1-(1-0.2^r))^b * M + (1-0.5^r)^b * N
for c in ((4,100),(4,1),(8,10),(6,100)):
  r = c[0]
  m = c[1]
  b = 24 / r
  print r, b, m
  print (1-math.pow(1-math.pow(0.2,r), b)) * m + math.pow(1-math.pow(0.5,r),b)

