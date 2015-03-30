import numpy
import time

tups = []
mindex = {}
uindex = {}
BASE_NAME = 'rating_1000'
for fname in ['%s_part_%d.csv' % (BASE_NAME, i) for i in range(4)]:
  with open(fname, 'r') as f:
    for i, line in enumerate(f):
      m, u, r = [s.strip() for s in line.split(",")]
      r = float(r)
      if m not in mindex:
        mindex[m] = len(mindex)
      if u not in uindex:
        uindex[u] = len(uindex)
      mi = mindex[m]
      ui = uindex[u]
      tups.append((mi, ui, r))

M = len(mindex)
U = len(uindex)
print "M:", M
print "U:", U
mat = numpy.zeros((M, U))
for i, j, r in tups:
  mat[i][j] = r

mb = numpy.where(mat > 0, 1, 0) # binarize to calc nij more easily
cu = numpy.sum(mb, axis=0)      # how many movies did this user rate
ci = numpy.sum(mb, axis=1)      # how many users rated this movie
ru = numpy.sum(mat, axis=0)
ri = numpy.sum(mat, axis=1)
LAMBDA = 1
A = numpy.vstack((
  numpy.concatenate(([numpy.sum(cu)], cu, ci)),
  numpy.concatenate((
    numpy.concatenate(([cu.T], numpy.diag(cu + LAMBDA), mb)).T,
    numpy.concatenate(([ci.T], mb.T, numpy.diag(ci + LAMBDA))).T
  ))
))
y = numpy.concatenate(([numpy.sum(ru)], ru, ri))
x = numpy.linalg.solve(A, y) # [mu ru1 ... ruU ri1 ... riM]
mu = x[0]
bu = x[1:U + 1]
bi = x[U + 1:]

#means = numpy.mean(mat, axis=1) # means[i] is the mean rating of movie i
means = numpy.sum(mat, axis=1) / ci
means_u = numpy.sum(mat, axis=0) / cu
bad_mu = numpy.sum(numpy.sum(mat)) / numpy.sum(cu)

def calc_nij(i, j):             # how many users rated both item i and j
  return numpy.dot(mb[i], mb[j])

def calc_sij(i, j):             # Pearson's coeff 
  x = (mat[i] - means[i]) * mb[i]
  y = (mat[j] - means[j]) * mb[j]
  if abs(numpy.dot(x, y)) < 0.001:
    return 0.
  return numpy.dot(x, y) / numpy.sqrt(numpy.dot(x, x) * numpy.dot(y, y))

def calc_dij(i, j, LAMBDA=100): # how similar are two items
  n = calc_nij(i, j)
  s = calc_sij(i, j)
  return s * n / (n + LAMBDA) 
  
def calc_bui(u, i):
  return mu + bu[u] + bi[i]

def calc_bad_bui(u, i):
  return bad_mu + means[i] + means_u[u]

dij_cache = {}

def get_top_dij(u, i, k=10):
  if i not in dij_cache:        
    # returns: a list of (dij, j)
    out = [(calc_dij(i, j), j) for j in range(M) if j != i]
    out.sort(reverse=True)
    out = tuple(out)
    dij_cache[i] = out
  out = []
  for dij, j in dij_cache[i]:
    if mat[j][u] > 0:         # user has seen item j(with good similarity to i )
      out.append((dij, j))
      if len(out) == k:
        break
  return out

def naive_est(u, i):
  if u is None:
    if i is None:
      return mu               # item not rated, user hasn't rated , guess!
    return mu + bi[i]
  if i is None:
    return mu + bu[u]
  dijs = get_top_dij(u, i)                                #n
  if sum([dij for dij, _ in dijs]) > 0:                   #n 
    return calc_bui(u, i) + sum([dij * (mat[j][u] - calc_bui(u, j)) for dij, j in dijs]) / sum([dij for dij, _ in dijs])#n
  return calc_bui(u, i)

def bad_naive_est(u, i):
  if u is None:
    if i is None:
      return mu               # item not rated, user hasn't rated , guess!
    return mu + bi[i]
  if i is None:
    return mu + bu[u]
#  dijs = get_top_dij(u, i)                               #bn
#  # ruj == mat[j][u]
#  if sum([dij for dij, _ in dijs]) > 0:
#    return calc_bad_bui(u, i) + sum([dij * (mat[j][u] - calc_bad_bui(u, j)) for dij, j in dijs]) / sum([dij for dij, _ in dijs])
  return calc_bad_bui(u, i)


# evaluate the goodness from the last partition
diffs = []
with open('%s_part_4.csv' % BASE_NAME, 'r') as f:
  for i, line in enumerate(f):
    m, u, r = [s.strip() for s in line.split(',')]
    mi = mindex.get(m, None)
    ui = uindex.get(u, None)
    diffs.append(float(r) - naive_est(ui, mi))         #g
#    diffs.append(float(r) - bad_naive_est(ui, mi))      #b
#    print float(r), naive_est(ui, mi)
    if i % 100 == 0:
      print i
  print sum([d ** 2 for d in diffs]) / len(diffs)

