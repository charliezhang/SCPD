import random
import time

d = 122
batch_size = 10

def load(file):
  f = open(file)
  r = [[float(i) for i in x.strip().split(',')] for x in f]
  f.close()
  return r

def cdot(a, b):
  assert(len(a) == len(b))
  return sum([a[i] * b[i] for i in xrange(0, len(a))])

def cost(w, b, C, x, y):
  r = 1.0 / 2 * sum([w[j] * w[j] for j in xrange(0, len(w))])
  for i in xrange(0, len(x)):
    r += C * max(0, 1 - y[i][0] * (cdot(x[i], w) + b))
  return r

def pred(w, b, x, y):
  return y[0] * (cdot(x, w) + b)

def fj(w, b, x, y, j):
  return sum([-y[i][0] * x[i][j] for i in xrange(0, len(x)) if pred(w, b, x[i], y[i]) < 1])

def fb(w, b, x, y):
  return sum([-y[i][0] for i in xrange(0, len(x)) if pred(w, b, x[i], y[i]) < 1])

def svm(x, y, C, eta, eps, mode):
  random.shuffle(x)
  w, b = [.0 for i in xrange(0, d)], .0
  n = len(x)
  last_c, delta_c = cost(w, b, C, x, y), .0
  i, l = 0, 0
  start = time.clock()
  times, costs = [], [] 
  while True: 
    if mode == 'sgd': bound = (i, i + 1)
    elif mode == 'mbgd': bound = (l * batch_size, (l + 1) * batch_size)
    else: bound = (0, n) # 'bgd'

    x2, y2 = x[bound[0]: bound[1]], y[bound[0]: bound[1]]

    for j in xrange(0, d):
      w[j] = w[j] - eta * (w[j] + C * fj(w, b, x2, y2, j))
    b = b - eta * C * fb(w, b, x2, y2)
    c = cost(w, b, C, x, y)
    per_c = abs(last_c - c) * 100 / last_c
    delta_c = .5 * delta_c + .5 * per_c

    #print 'Mode: %s, Cost: %f, Perc_C: %f, Delta_Cost: %f, Time: %f' % (mode, c, per_c, delta_c, time.clock() - start)
    if (mode == 'bgd' and per_c < eps) or delta_c < eps:
      break
    last_c = c
    i = (i + 1) % n
    l = (l + 1) % (n / batch_size)
    times.append(time.clock() - start)
    costs.append(c)
  #print 'Mode %s, num iter %d\n time:\n%s\ncosts:\n%s\n' % (mode, len(times), str(times), str(costs))
  return w, b

def error(w, b, x, y):
  return len([i for i in xrange(0, len(x)) if pred(w, b, x[i], y[i]) < 1]) / float(len(x))

def main():
  x = load('q1-data/features.txt')
  y = load('q1-data/target.txt')
  #x = load('features.small.txt')
  #y = load('targets.small.txt')
  assert(len(x) == len(y))
  assert(len(x[0]) == d)

  ''' q1 - (e)
  svm(x, y, 100, 0.0000003, 0.25, 'bgd')
  svm(x, y, 100, 0.0001, 0.001, 'sgd')
  svm(x, y, 100, 0.000001, 0.01, 'mbgd')
  '''

  ''' q1 - (f) '''
  x_train = load('q1-data/features.train.txt')
  y_train = load('q1-data/target.train.txt')
  x_test = load('q1-data/features.test.txt')
  y_test = load('q1-data/target.test.txt')
  E = []
  for C in [1, 10, 50, 100, 200, 300, 400, 500]:
    w, b = svm(x_train, y_train, C, 0.0001, 0.001, 'sgd')
    e_train = error(w, b, x_train, y_train)
    e = error(w, b, x_test, y_test)
    print "C: %d, Errors: %f, %f\n" % (C, e_train, e)
    E.append(e)
  print E


if __name__ == '__main__': 
  main()
