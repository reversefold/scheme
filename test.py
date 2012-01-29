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
        "(> 1 3)",
        "(> 3 1)",
        "(< 1 3)",
        "(< 3 1)",
        "(if (< 1 3) 'y 'n)",
        "(if (> 1 3) 'y 'n)",
        "(if (< 1 3) (+ 1 3) (- 1 3))",
        "(if (> 1 3) (+ 1 3) (- 1 3))",
        """
(cond ((> 3 2) 'greater)
      ((< 3 2) 'less))""",
        """
(cond ((> 2 3) 'greater)
      ((< 2 3) 'less))""",
        """
(cond ((> 3 3) 'greater)
      ((< 3 3) 'less)
      (else 'equal))""",
        """
(cond (#f 1)
      (#t 2)
      (#t 3))""",

        "(* 1 1)",
        "(* 5 7)",
        "(/ 1 1)",
        "(/ 1 2)",
        "(/ 42 2)",

        "(and #t #t)",
        "(and #t #f)",
        "(and #f #f)",
        "(and (> 3 1) (< 1 3))",
        "(and (> 3 1) (> 1 3))",

        "(or #t #t)",
        "(or #t #f)",
        "(or #f #f)",
        "(or (> 3 1) (< 1 3))",
        "(or (> 3 1) (> 1 3))",

        """
(case (* 2 3)
      ((2 3 5 7) 'prime)
      ((1 4 6 8 9) 'composite))""",
#        """
#(case (car '(c d))
#      ((a) 'a)
#      ((b) 'b))""",
        """
(case (car '(c d))
      ((a e i o u) 'vowel)
      ((w y) 'semivowel)
      (else 'consonant))""",
        '(quote (1 2 3))'
        ]:
    print "Input: %s" % expr
    token = SchemeParser(expr).parse()
    print "Token: %s" % token
    s = Scheme(token)
    print "Value: %s\n" % (s.eval(),)
