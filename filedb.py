from sage.all import *
from polynomial import *
import os
#from sage.rings.rational_field import QQ
#import sage.all

class FileDB():
  """
  File database for polynomials and its normalized roots
  """

  def __init__(self):
    self.db_dir = "./data/"
    self.degree_prefix = "degree"
    self.gid_prefix = "id"

  def add(self, f):
    """
    Adds a polynomial to the database by creating a file

    INPUT:
      f -- Irreducible polynomial over rationals
    """
    # f needs to be irreducible
    if not f.is_irreducible():
      print f, "is not irreducible."
      return
    else:
      fname = self.poly_to_fname(f)
      fdb = open(fname, 'w')
      fdb.close()


  def list(self, degree=None, info=False, dictionary=False):
    """
    Lists polynomials in the database
    
    INPUT:
      degree [optional] -- List only the polynomials of degree
      info [optional] -- Returns list of [d,g,f] where d = degree of f, g =
                         Galois group id of f, f a polynomial
      dictionary [optional] -- Returns a dictionary of dictionary of lists
                               Top dictionary has degrees as keys
                               Second dictionary has Galois group id as keys
                               Lists contain polynomial functions

    """
    files = os.listdir(self.db_dir)

    if dictionary:
      info = True

    lst = list()
    for path in files:
      d = self.fname_to_poly(path, info=True)
      if not degree or degree == d[0]:
        if info:
          lst.append(d)
        else:
          lst.append(d[2])

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
    lst = self.list(degree, info=True)
    
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

      print " ("+str(j)+") ", lst[i][2], " ["+str(self.load_roots(lst[i][2], count=True))+"]"

      j += 1
      

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
    return int(f.split("/")[-1].split("_")[0][len(self.degree_prefix):])

  def gid(self, f):
    if type(f) == str: # Filename
      return int(f.split("/")[-1].split("_")[1][len(self.gid_prefix):])
    else:
      return str(f.galois_group()).split()[3]

  def load_roots(self, f, count=False):
    fname = self.poly_to_fname(f)

    if not os.path.isfile(fname):
      print "Error: ", f, "does not exist in the database"

    elif os.path.getsize(fname) == 0:
      if count:
        return 0
      else:
        return []

    else:
      if count:
        with open(fname) as fdb:
          for i, l in enumerate(fdb):
            pass
          return i + 1
      else:
        roots = list()
        fdb = open(fname, 'r')
        for line in fdb:
          roots.append(QQ(line.split()[0])/QQ(line.split()[1]))

        return roots

  def save_roots(self, n, degree=None, gid=None, j=None, f=None):
    if degree and gid and j:
      f = self.load(degree, gid, j)
    elif f == None:
      print "Error: arguments: (n, f) or (n, degree, gid, j)"

    p = self.last_prime(f)
    fname = self.poly_to_fname(f)

    count = 0
    # Record one at a time
    for i in range(0,n):
      fdb = open(fname, 'a')
      for q in roots_modp(f, p):
        fdb.write(str(q.numerator()) + " " + str(q.denom()) + "\n")
        count += 1

      fdb.close()
      p = next_prime(p)
      print >> sys.stderr, p,

    print

    return count


  def last_prime(self, f):
    fname = self.poly_to_fname(f)
    if not os.path.isfile(fname):
      fdb = open(fname, 'w')
      fdb.close()
      p = 0
    elif os.path.getsize(fname) == 0:
      p = 0
    else:
      for line in open(fname):
        pass
      p = QQ(line.split()[1])

    return p

  def density_plot(self, f, precision=50, start=0, stop=0):
    density = self.density(f, precision)
    
    total = 0
    for i in density.keys():
      total += density[i]

    interval = 1/QQ(precision)
    lst = list()
    for i in density.keys():
      lst.append(((i+0.5)*interval, density[i]/QQ(total)))

    return scatter_plot(lst, markersize=3)

  def density(self, f, precision=50):
    roots = self.load_roots(f)
    
    count = dict()
    for i in range(0,precision):
      count[i] = 0

    interval = QQ(1) / QQ(precision)
    for i in range(0, precision):
      low = i*interval
      high = (i + 1) * interval
      
      for r in roots:
        if low <= r < high:
          count[i] += 1

    return count

  def flat_plot(self, f, limit=None):
    colors = ["#FF0000", "#000000", "#FFFF00", "#0000FF", "#FF00FF", "#808080",
              "#008000", "#00FF00", "#800000", "#000080", "#808000", "#800080", 
              "#C0C0C0", "#00FFFF", "#008080"]
    
    if type(f) != list:
      f = [f]

    # Empty plot
    plot = scatter_plot([])

    # For color coordination
    classes = list()

    for i in range(len(f)):
      # Identify a class of f by degree, group id tuple
      degree = f[i].degree()
      gid = self.gid(f[i])
      id = (degree, gid)
      if classes.count(id) == 0:
        classes.append(id)
      color = classes.index(id)

      # Generate Plots
      roots = self.load_roots(f[i])[:limit]
      points = [(j,i+0.5) for j in roots]
      plot_opts = {'markersize':10, 
                   'facecolor':colors[color], 'edgecolor':colors[1]}
      plot += scatter_plot(points, **plot_opts)

      # Labels
      count = len(roots)
      if limit and count == limit:
        if i == (len(f) - 1):
          plot += text(str(count), (1,i+0.8), horizontal_alignment='right')
        label = "D" + str(degree) + "G" + str(gid)
      else:
        label = "D" + str(degree) + "G" + str(gid) + "(" + str(count) + ")" 

      label_opts = {'fontsize':8, 'rgbcolor':(20,20,20),
                    'horizontal_alignment':'left'}
      plot += text(label, (0.01,i+0.8), **label_opts)

    return plot

  def animate_flat_plot(self, f, step=10, limit=None, figsize=[15,2]):

    # Figure out how many frames we will have
    # ...not very efficient
    max = 0
    for i in range(len(f)):
      n = len(self.load_roots(f[i]))
      if max < n:
        max = n

    if (limit and max < limit) or not limit:
      limit = max
    frames = int(limit/step) + 1

    plots = list()
    for i in range(frames):
      j = (i + 1) * step
      plots.append(self.flat_plot(f, j))

    return animate(plots, figsize=figsize)
