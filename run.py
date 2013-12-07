from scheme import Scheme
from scheme.parser import SchemeParser
import sys


def main():
    expression = sys.stdin.read()

    print "Input:    %s" % (expression,)
    token = SchemeParser(expression).parse()
    print "Token:    %s" % (token,)
    s = Scheme(token)
    result = s.ceval()
    print "Value:    %s" % (result,)


if __name__ == '__main__':
    main()
