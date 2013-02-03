#!/usr/bin/env python

import math

def dist(a, b):
  return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def dist2(a, b):
  return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

def split(a, b, pts):
  seta = []
  setb = []
  for p in pts:
    if dist(a, p) < dist(b, p):
      seta.append(p)
    else:
      setb.append(p)
  return seta, setb

def error(pts):
  e = 0
  x = 0.0
  y = 0.0
  for p in pts:
    x += p[0]
    y += p[1]
  c = (x / len(pts), y / len(pts))
  print "Computing error for centroid %s" % str(c)
  for p in pts:
    e += dist2(c, p)
  return e

pts = [(-1,-1)]
for i in (2, 1, 0):
  for j in (0, 1, 2):
    pts.append((j, i))
choice = [(3, 7), (1, 2), (2, 7)]
for c in choice:
  print "Choosing centroids: " + str(c)
  seta, setb = split(pts[c[0]], pts[c[1]], pts[1:])
  print "Set A: " + str(seta)
  print "Set B: " + str(setb)
  print error(seta) + error(setb)

selected = [(0, 0), (10, 10)]
pts = [(1,6), (3,7), (4,3), (7,7), (8,2), (9,5)]
for i in range(1, 6):
  max = -1
  maxp = None
  for p in pts:
    if p not in selected:
      min = 9999
      for s in selected:
        d = dist(s, p)
        if d < min:
          min = d
    if min > max:
      max = min
      maxp = p
  print "Max distance = %f selecting %s" % (max, str(maxp))
  selected.append(maxp)

print selected
      

