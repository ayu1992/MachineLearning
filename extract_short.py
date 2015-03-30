with open("/Volumes/YUCHI/ML_anan/movies.txt.txt.txt", "r") as f:
  with open("summary_rating.csv", "w") as of:
    arr = ["", "", "", ""]
    for i, line in enumerate(f):
      if i % 100000 == 0:
        print i
      if line.startswith("product/productId"):
        arr[0] = line.split()[1]
      elif line.startswith("review/userId"):
        arr[1] = line.split()[1]
      elif line.startswith("review/score"):
        arr[2] = line.split()[1]
      elif line.startswith("review/summary"):
        arr[3] = ' '.join(line.split()[1:])
        of.write(", ".join(arr) + "\n")

