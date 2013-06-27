
import sys

def get_distance(v1, v2):
  r = 0.0
  for i in range(0, len(v1)): 
    r += (v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2
  return r

def get_second_point(file):
  f = open(file)
  cnt = 0
  for line in f:
   
    if cnt == 1:
      p = line.strip().split(" ")
      p = map(lambda x: float(x), p)
      f.close()
      return p
    cnt += 1

def get_centroids(file):
  f = open(file)
  list = []
  for line in f:
    c = line.strip().split(":")[0].split(" ")
    list.append(map(lambda x: float(x), c))
  f.close()
  return list


def main():
  data_file = sys.argv[1]
  cent_file = sys.argv[2]
  p2 = get_second_point(data_file)
  cent = get_centroids(cent_file)
  c2 = None
  minD = -1
  for c in cent:
    d = get_distance(p2, c)
    if minD < 0 or d < minD:
      minD = d
      c2 = c
  print "Centroid for p2: " + str(c2)
  list = []
  for i in range(0, len(c2)):
    list.append((i, c2[i]))
  list = sorted(list, key=lambda x: x[1], reverse=True)
  print "Sorted features and idx: " + str(list)


if __name__ == '__main__':
  main()
