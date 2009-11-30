load polynomial.sage

def test_group():
  for i in range(1):
    f = irreducible_polynomial(5)
    f.galois_group()

def test_discriminant():
  for i in range(1):
    f = irreducible_polynomial(5)
    a = f.discriminant()
    print a.is_square()

if __name__=='__main__':
  from timeit import Timer
  t = Timer("test_group()", "from __main__ import test_group")
  p = Timer("test_discriminant()", "from __main__ import test_discriminant")
  print "discriminant:", p.timeit(number=10000)
  print "group:", t.timeit(number=10000)
