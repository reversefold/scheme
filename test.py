from scheme import Scheme
from scheme.parser import SchemeParser

for expression, expected in [
        ('(+ 1 2)', '3'),
        ('(- 3 2)', '1'),
        ("(car '(1 2 3))", '1'),
        ("(cdr '(1 2 3))", '(2 3)'),
        ("(cons 3 '(1 2))", '(3 1 2)'),
        ("(cons (+ 1 (- 3 (+ 15 34))) '(4 5))", '(-45 4 5)'),
        ("(cons (+ 1 (- 3 (+ 15 34))) '(4 (+ 4 5)))", '(-45 4 (+ 4 5))'),

        ("#t", '#t'),
        ("#f", '#f'),
        ('(quote #t)', '#t'),
        ("'#t", '#t'),
        ("'#f", '#f'),
        ("(if #t 'y 'n)", "y"),
        ("(if #f 'y 'n)", "n"),
        ("(if '1 'y 'n)", "y"),

        ("(> 1 3)", '#f'),
        ("(> 3 1)", '#t'),
        ("(< 1 3)", '#t'),
        ("(< 3 1)", '#f'),

        ("(if (< 1 3) 'y 'n)", "y"),
        ("(if (> 1 3) 'y 'n)", "n"),
        ("(if (< 1 3) (+ 1 3) (- 1 3))", '4'),
        ("(if (> 1 3) (+ 1 3) (- 1 3))", '-2'),

        ("""
(cond ((> 3 2) 'greater)
      ((< 3 2) 'less))""", "greater"),
        ("""
(cond ((> 2 3) 'greater)
      ((< 2 3) 'less))""", "less"),
        ("""
(cond ((> 3 3) 'greater)
      ((< 3 3) 'less)
      (else 'equal))""", "equal"),
        ("""
(cond (#f 1)
      (#t 2)
      (#t 3))""", '2'),

        ("(* 1 1)", '1'),
        ("(* 5 7)", '35'),
        ("(/ 1 1)", '1'),
        ("(/ 1 2)", '1/2'),
        ("(/ 42 2)", '21'),

        ("(and #t #t)", '#t'),
        ("(and #t #f)", '#f'),
        ("(and #f #t)", '#f'),
        ("(and #f #f)", '#f'),
        ("(and (> 3 1) (< 1 3))", '#t'),
        ("(and (> 3 1) (> 1 3))", '#f'),

        ("(or #t #t)", '#t'),
        ("(or #t #f)", '#t'),
        ("(or #f #t)", '#t'),
        ("(or #f #f)", '#f'),
        ("(or (> 3 1) (< 1 3))", '#t'),
        ("(or (> 3 1) (> 1 3))", '#t'),

        ("""
(case (* 2 3)
      ((2 3 5 7) 'prime)
      ((1 4 6 8 9) 'composite))""", "composite"),
        ("""
(case (car '(c d))
      ((a) 'a)
      ((b) 'b))""", 'None'),
        ("""
(case (car '(c d))
      ((a e i o u) 'vowel)
      ((w y) 'semivowel)
      (else 'consonant))""", "consonant"),
        ('(quote (1 2 3))', "(1 2 3)"),
        ]:
    token = SchemeParser(expression).parse()
    s = Scheme(token)
    result = s.eval()
    if str(result) != expected:
        print "Input:    %s" % expression
        print "Token:    %s" % token
        print "Value:    %s" % (result,)
        print "Expected: %s\n" % (expected,)
