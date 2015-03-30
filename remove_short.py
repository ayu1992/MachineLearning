from collections import Counter

M_THRESH = 400 # min cnt of ratings for movie
U_THRESH = 400 # min cnt of ratings for user
mctr = Counter()
uctr = Counter()
rctr = Counter()

print "Counting..."
with open("rating_only.csv", "r") as f:
  for i, line in enumerate(f):
    m, u, r = [s.strip() for s in line.split(',')]
    mctr[m] += 1
    uctr[u] += 1
    rctr[r] += 1
    if i % 100000 == 0:
      print i

print "Movie:", sum([1 for v in mctr.values() if v >= M_THRESH]), len(mctr)
print "User:", sum([1 for v in uctr.values() if v >= U_THRESH]), len(uctr)
#print rctr
"""
Movie: 71750 253059
User: 60181 889176
Counter({'5.0': 4380544, '4.0': 1654815, '3.0': 791594, '1.0': 629332, '2.0': 455399})
"""

print "Writing..."
with open("rating_only.csv", "r") as f:
  with open("rating_%d_%d.csv" % (M_THRESH, U_THRESH), "w") as of:
    for i, line in enumerate(f):
      m, u, r = [s.strip() for s in line.split(',')]
      if mctr[m] >= M_THRESH and uctr[u] >= U_THRESH:
        of.write(", ".join([m, u, r]) + "\n")
      if i % 100000 == 0:
        print i


print "Done"
