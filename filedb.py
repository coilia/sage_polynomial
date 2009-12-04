from sage.all import *
from polynomial import *
import os
#from sage.rings.rational_field import QQ
#import sage.all

class FileDB():
  """
  """

  def __init__(self):
    self.db_dir = "./data/"
    self.degree_prefix = "degree"
    self.gid_prefix = "id"

  def list(self, degree=False, dictionary=False):
    files = os.listdir(self.db_dir)

    lst = list()
    for path in files:
      d = self.fname_to_poly(path, info=True)
      if not degree or degree == d[0]:
        lst.append(d)

    # This sorts by degree, gid, coeffcients
    lst.sort()

    if dictionary:
      dic = dict()
      for i in lst:
        if not dic.has_key(i[0]):
          dic[i[0]] = dict()

        if not dic[i[0]].has_key(i[1]):
          dic[i[0]][i[1]] = list()

        dic[i[0]][i[1]].append(i[2])

      return dic

    else:
      return lst

  def show(self, degree=False):
    lst = self.list(degree)
    
    current_degree = 0
    current_group = 0
    j = 1
    for i in range(len(lst)):
      if current_degree != lst[i][0]:
        current_degree = lst[i][0]
        current_group = 0
        print ""
        print "Degree ", current_degree

      if current_group != lst[i][1]:
        current_group = lst[i][1]
        j = 1
        print ""
        print "Galois Group:", current_group

      print " ("+str(j)+") ", lst[i][2], " ["+str(self.count_roots(lst[i][2]))+"]"

      j += 1
      
  def count_roots(self, f):
    fname = self.poly_to_fname(f)
    
    if os.path.isfile(fname):
      with open(fname) as fdb:
        for i, l in enumerate(fdb):
          pass
        count = i + 1
    else:
      count = 0

    return count

  def load(self, degree, gid, j):
    return self.list(degree, dictionary=True)[degree][gid][j-1]

  def poly_to_fname(self, f):

    # Read coefficients
    c = str()
    for i in f.coeffs():
      c += "_" + str(i)

    degree = str(f.degree())
    
    # Find out Galois group id
    gid = self.gid(f)
    try:
      int(gid)
    except:
      print "Error reading Galois group id"

    fname = self.degree_prefix + degree + "_" + self.gid_prefix + gid + c
    return self.db_dir + fname

  def fname_to_poly(self, fname, info=False):
    degree = self.degree(fname)
    gid = self.gid(fname)

    name = fname.split("_")
    c = list()
    for i in name[2:]:
      try:
        i = QQ(i)
      except:
        print "Error reading file name of: ", fname

      c.append(i)

    # Integrity Checks
    if degree != (len(c) - 1):
      print "Degree and number of coefficients do not match in: ", fname

    # Make polynomial, check galois group
    f = make_polynomial(c)
    if gid != int(str(f.galois_group()).split()[3]):
      print gid
      print f.galois_group()
      print "Galois group does not match: ", fname

    if info:
      return [degree, gid, f]
    else:
      return f

  def degree(self, f):
    return int(f.split("_")[0][len(self.degree_prefix):])

  def gid(self, f):
    if type(f) == str: # Filename
      return int(f.split("_")[1][len(self.gid_prefix):])
    else:
      return str(f.galois_group()).split()[3]
