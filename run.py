from scheme import Scheme
from scheme.parser import SchemeParser
import sys

expression = sys.stdin.read()

print "Input:    %s" % (expression,)
token = SchemeParser(expression).parse()
print "Token:    %s" % (token,)
s = Scheme(token)
result = s.ceval()
print "Value:    %s" % (result,)
