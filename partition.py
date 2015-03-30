import random
import sys

if len(sys.argv) != 3:
  raise ValueError('args are num of partitions and input filename')

N = int(sys.argv[2])

ofs = [open('%s_part_%d.%s' % (sys.argv[1].split('.')[0], i, sys.argv[1].split('.')[1]), 'w') for i in range(N)]

with open(sys.argv[1], 'r') as f:
  for line in f:
    i = random.randint(0, N - 1)
    ofs[i].write(line)
for f in ofs:
  f.close()
