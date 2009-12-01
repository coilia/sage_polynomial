load polynomial.sage
import os.path

def test_discriminant(f):
  return f.discriminant().is_square()

def bruteforce(d, limit, record=False, filename='default', min=-100, max=100):

  if record:
    if filename == "default":
      filename = "degree" + str(d)

    if not os.path.isfile(filename):
      fdb = open(filename, 'w')
      fdb.close()

    fdb = open(filename, 'a')

  tried = 0
  tried_hundred = 0
  found = 0

  while found < limit:
    f = irreducible_polynomial(d)
    if test_discriminant(f):
      print
      print "Tried: ", tried, "polynomials"
      print "f(x) = ", f
      
      if record:
        line = str()
        for i in f.coeffs():
          line += str(i) + ' '

        fdb.write(line + "\n")

      found += 1
    
    tried += 1
    if tried_hundred != int(tried / 100):
      print >> sys.stderr, tried, 
      tried_hundred = int(tried / 100)

  if record:
    fdb.close()

def check(d, filename='default'):
  if filename == 'default':
    filename = "degree" + str(d)

  if not os.path.isfile(filename):
    print "The file " + filename + " does not exists."
  else:
    fdb = open(filename, 'r')

    for line in fdb:
      c = [int(i) for i in line.split()]
      f = make_polynomial(c)
      print f.galois_group()

  return 0
