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

  def listfiles(self, degree=False):
    files = os.listdir(self.db_dir)

  def list(self, degree=False):
    files = os.listdir(self.db_dir)

    lst = list()
    for path in files:
      line = self.fname_to_poly(path,extra=True)
      if not degree or degree == line[0]:
        lst.append(line)

    # This sorts by degree, gid, coeffcients
    lst.sort()
    
    current_degree = 0
    current_group = 0
    j = 1
    for i in range(len(lst)):
      if current_degree != lst[i][0]:
        current_degree = lst[i][0]
        current_group = 0
        j = 1
        print ""
        print "Degree ", current_degree

      if current_group != lst[i][1]:
        current_group = lst[i][1]
        print ""
        print "Galois Group:", current_group

      print "   ("+str(j)+") ", lst[i][2], " ("+str(self.count_roots(lst[i][2]))+")"

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

  def load(self, degree, j):
    return

  def poly_to_fname(self, f):

    # Read coefficients
    c = str()
    for i in f.coeffs():
      c += "_" + str(i)

    degree = str(f.degree())
    
    # Find out Galois group id
    gid = str(f.galois_group()).split()[3]
    try:
      int(gid)
    except:
      print "Error reading Galois group id"

    fname = self.degree_prefix + degree + "_" + self.gid_prefix + gid + c
    return self.db_dir + fname

  def fname_to_poly(self, fname, extra=False):
    name = fname.split("_")
    degree = int(name[0][6:])
    gid = int(name[1][2:])
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

    if extra:
      return [degree, gid, f]
    else:
      return f
