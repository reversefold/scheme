from scheme import Scheme
from scheme.parser import SchemeParser

for expr in [
        '(+ 1 2)',
        '(- 3 2)',
        "(car '(1 2 3))",
        "(cdr '(1 2 3))",
        "(cons 3 '(1 2))",
        "(cons (+ 1 (- 3 (+ 15 34))) '(4 5))",
        "(cons (+ 1 (- 3 (+ 15 34))) '(4 (+ 4 5)))",
        "#t",
        "#f",
        "(if #t 'y 'n)",
        "(if #f 'y 'n)",
        "(if '1 'y 'n)",
        ]:
    print "Input: %s" % expr
    token = SchemeParser(expr).parse()
    print "Token: %s" % token
    s = Scheme(token)
    print "Value: %s\n" % s.eval()
