import os.path

def random_coefficients(n, min=-100, max=100):
  """ 
  random_coefficients(n, min=-100, max=100)
    n - positive integer
    min - integer
    max - integer

  returns [i_1, i_2, ..., i_n] 
    where i_j are random integers between min and max
  """

  return [randint(min,max) for i in range(0,n)]


def make_polynomial(c):
  """ 
  make_polynomial(c)
    c - list =  [c_0, c_1, ..., c_n]

  returns f
    where f = c_n*x^n + ... + c_1*x + c_0
  """
  R.<x> = QQ[]
  f = x-x

  for i in range(0, len(c)):
    f = f + c[i]*x^i

  return f

def random_polynomial(d, min=-100, max=100):
  """ 
  random_polynomial(d)
    d - positive integer
    min - integer
    max - integer

  returns f
    where f is degree d polynomial with random coefficients between min and max
  """

  c = random_coefficients(d+1, min, max)
  f = make_polynomial(c)
  while not f.degree(x) == d:
    c = random_coefficients(d+1, min, max)
    f = make_polynomial(c)

  return f

def irreducible_polynomial(d, min=-100, max=100):
  """
  irreducible_polynomial(d)
    d - positive integer
    min - integer
    max - integer

  returns f
    where f is degree d, irreducible polynomial with random coefficients between
    min and max
  """

  # constant polynomial
  if d == 0:
    return 0

  f = random_polynomial(d, min, max)
  while not f.is_irreducible():
    f = random_polynomial(d, min, max)

  return f

def integerize_coefficients(f):
  """
  integerize_coefficients(f)
    f - polynomial

  returns None
    multiplies lcm of denominators
  """
    
  d = list()

  # Use f.coefficients() since this omitts zero coefficients
  for c in f.coefficients():
    if c.denominator() != 1:
      d.append(c.denominator())
  
  f = lcm(d)*f

  return None

def roots_mod(f, n):
  """ 
  roots_mod(f,n)
    f - polynomial
    n - integer

  returns [r_1, r_2,...r_n] 
    where f(r_i) === 0 mod n
  """
  var('y') # need to use a variable for solve_mod
  roots = solve_mod(f(y) == 0, n)

  sol = []
  for i in roots:
    if i[0] > 0:
      sol.append(i[0])

  return sol

def roots_modp(f, p, n=1):
  """
  roots_modp(f, p1, p2)
    f - polynomial
    p - prime number
    n - positive integer

  returns [r_1/p_1, r_2/p_2, ..., r_n/p_n]
    where f(r_i) = 0 mod p_i
    and p1 <= p_i <= p2
  """
  if not is_prime(p):
    p = next_prime(p)

  rootsp = []
  for i in range(0,n):
    roots = roots_mod(f, p)
    for r in roots:
      rootsp.append(QQ(r)/QQ(p))
    p = next_prime(p)

  return rootsp

def db_filename(f):
  """
  db_filename(f)
    f - polynomial

  returns string
    filename composed of degree, galois group id, and coefficients
  """
  filename = "../data/"
  filename += "degree" + str(f.degree()) + "_"
  filename += "id" + str(f.galois_group()).split()[3]
  c = f.coeffs()
  for i in c:
    filename += "_" + str(i)

  return filename

def db_record_roots(f, n=10):
  """
  
  """

  p = next_prime(db_read_last(f))

  filename = db_filename(f)

  if not os.path.isfile(filename):
    fdb = open(filename, 'w')
    fdb.close()
  fdb = open(filename, 'a')

  count = 0
  # Record one at a time
  for i in range(0,n):
    for q in roots_modp(f, p):
      fdb.write(str(q.numerator()) + " " + str(q.denom()) + "\n")
      count += 1

    p = next_prime(p)
    print >> sys.stderr, p,

  print

  fdb.close()

  return count

def db_read_last(f):
  

  filename = db_filename(f)
  if not os.path.isfile(filename):
    fdb = open(filename, 'w')
    fdb.close()
    p = 0
  else:
    for line in open(filename):pass
    p = QQ(line.split()[1])

  return p

def db_load(f):
  filename = db_filename(f)
  if not os.path.isfile(filename):
    print >> sys.stderr, "Database for this polynomial does not exist."
    return 

  roots = []
  fdb = open(filename, 'r')
  for line in fdb:
    r = QQ(line.split()[0])
    p = QQ(line.split()[1])
    roots.append(r/p)

  fdb.close()

  return roots

def dumbplot(f, n=0):
  if n == 0:
    roots = db_load(f)
  else:
    roots = roots_modp(f,2,n)

  return scatter_plot([(i,0) for i in roots], markersize=3)

def density(f, precision=10, start=0, stop=0):
  if stop == 0:
    roots = db_load(f)
  else:
    roots = db_load(f)[start:stop]
  
  count = dict()
  for i in range(0,precision):
    count[i] = 0

  interval = 1 / precision.n()
  for i in range(0, precision):
    low = i*interval
    high = (i + 1) * interval
    for r in roots:
      if low <= r < high:
        count[i] += 1

  return count

def density_plot(f, precision=10, normalize=False, start=0, stop=0):

  count = density(f, precision, start, stop)

  if normalize:
    total = 0
    for i in count.keys():
      total += count[i]
  else:
    total = 1

  if stop == 0:
    stop = count.keys()[-1]

  interval = 1/precision.n()
  lst = list()
  for i in count.keys():
    lst.append(((i+0.5)*interval, count[i]/total))

  return scatter_plot(lst, markersize=3)

def animate_density(f, precision=10, steps=10):
  count = density(f, precision)

  total = 0
  for i in count.keys():
    total += count[i]

  frames = (total / steps) + 1
  plots = list()
  for i in range(0,frames):
    plots.append(density_plot(f, precision, False, 0, (i + 1) * steps))

  return animate(plots)
