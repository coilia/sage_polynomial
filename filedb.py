import os
#from sage.rings.rational_field import QQ
import sage.all

class filedb():
  """
  """

  def __init__(self):
    self.db_dir = "./data/"
    self.degree_prefix = "degree"
    self.gid_prefix = "id"

  def list(self):
    files = os.listdir(self.db_dir)

    for path in files:
      print self.filename_to_poly(path)

  def load(self, degree):
    return

  def poly_to_filename(self, f):

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
      print("Error reading Galois group id")

    filename = self.degree_prefix + degree + "_" + self.gid_prefix + gid + c
    return self.db_dir + filename

  def filename_to_poly(self, filename):
    name = filename.split("_")
    degree = int(name[0][6:])
    gid = int(name[1][2:])
    c = list()
    for i in name[2:]:
      try:
        i = QQ(i)
      except:
        print("Error reading file name of: ", filename)

      c.append(i)

    # Integrity Checks
    if degree != (len(c) - 1):
      print("Degree and number of coefficients do not match in: ", filename)

    # Make polynomial, check galois group

    return c
