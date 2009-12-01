load polynomial.sage

d = 4

def test_discriminant(f):
  return f.discriminant().is_square()

if __name__=='__main__':
  count = 0
  a = 0
  while true:
    f = irreducible_polynomial(d)
    if test_discriminant(f):
      print "Count: ", count
      print "f(x) = ", f
      break
    
    count += 1
    if a != int(count / 100):
      print >> sys.stderr, count, 
      a = int(count / 100)
