from scheme import Scheme
from scheme.parser import SchemeParser
import sys
    
#(lambda (dragon rcons i) (dragon dragon rcons i))
# (lambda (dragon rcons i)
#   (cond
#    ((= i 0) '())
#    (else
#     ((lambda (interp-rl rcons d c) (interp-rl interp-rl rcons d c))
#      (lambda (interp-rl rcons d c)
#        (cond
#         ((null? d) '(r))
#         ((= 1 (length d)) (cons c (rcons (if (equal? 'r c) 'l 'r) d)))
#         (else
#          (cons
#           c
#           (rcons
#            (if (equal? 'r c) 'l 'r)
#            (cons
#             (car d)
#             (rcons
#              ((lambda (f a) (f f a)) (lambda (rcar l) (cond ((= 1 (length l)) (car l)) (else (rcar rcar (cdr l))))) d)
#              (interp-rl
#               interp-rl
#               rcons
#               ((lambda (f a) (f f a)) (lambda (rcdr l) (cond ((= 1 (length l)) '()) (else (cons (car l) (rcdr rcdr (cdr l)))))) (cdr d))
#               (if (equal? 'r c) 'l 'r)))))))))
#      rcons
#      (dragon dragon rcons (- i 1))
#      'r))))
# (lambda (v l) ((lambda (rcons v l) (rcons rcons v l)) (lambda (rcons v l) (cond ((null? l) (list v)) (else (cons (car l) (rcons rcons v (cdr l)))))) v l))

#(define (rcar l) (cond ((= 1 (length l)) (car l)) (else (rcar (cdr l)))))
#(define (rcdr l) (cond ((= 1 (length l)) '()) (else (cons (car l) (rcdr (cdr l))))))
#(define (rcons v l) (cond ((null? l) (list v)) (else (cons (car l) (rcons v (cdr l))))))

# r r l r r l l r r r l l r l l r r r l r r l l l r r l l r l l
#   r   r   l   r   r   l   l   r   r   r   l   l   r   l   l
#       r       r       l       r       r       l       l
#               r               r               l
#                               r

dragon = open('dragon.scm', 'r').read()

expressions = [
#    ('3', '3'),
#
#    ("#t", '#t'),
#    ("#f", '#f'),
#    ('(quote #t)', '#t'),
#    ("'#t", '#t'),
#    ("'#f", '#f'),
#
#    ('(+ 1 2)', '3'),
#    ('(- 3 2)', '1'),
#    ("(car '(1 2 3))", '1'),
#    ("(cdr '(1 2 3))", '(2 3)'),
#    ("(car (cdr '(1 2 3)))", '2'),
#    ("(cons 3 '(1 2))", '(3 1 2)'),
#    ("(cons (+ 1 (- 3 (+ 15 34))) '(4 5))", '(-45 4 5)'),
#    ("(cons (+ 1 (- 3 (+ 15 34))) '(4 (+ 4 5)))", '(-45 4 (+ 4 5))'),
#    ("(cons (car '(1 2 3)) (cdr '(4 5 6)))", "(1 5 6)"),
#
#    ("(> 1 3)", '#f'),
#    ("(> 3 1)", '#t'),
#    ("(< 1 3)", '#t'),
#    ("(< 3 1)", '#f'),
#    
#    ("(and #t #t)", '#t'),
#    ("(and #t #f)", '#f'),
#    ("(and #f #t)", '#f'),
#    ("(and #f #f)", '#f'),
#    ("(and (> 3 1) (< 1 3))", '#t'),
#    ("(and (> 3 1) (> 1 3))", '#f'),
#    
#    ("(or #t #t)", '#t'),
#    ("(or #t #f)", '#t'),
#    ("(or #f #t)", '#t'),
#    ("(or #f #f)", '#f'),
#    ("(or (> 3 1) (< 1 3))", '#t'),
#    ("(or (> 3 1) (> 1 3))", '#t'),
#
#    ("(if #t 'y 'n)", "y"),
#    ("(if #f 'y 'n)", "n"),
#    ("(if '1 'y 'n)", "y"),
#
#    ("(if (< 1 3) 'y 'n)", "y"),
#    ("(if (> 1 3) 'y 'n)", "n"),
#    ("(if (< 1 3) (+ 1 3) (- 1 3))", '4'),
#    ("(if (> 1 3) (+ 1 3) (- 1 3))", '-2'),
#
#    ("""
#(cond ((> 3 2) 'greater)
#      ((< 3 2) 'less))""", "greater"),
#    ("""
#(cond ((> 2 3) 'greater)
#      ((< 2 3) 'less))""", "less"),
#    ("""
#(cond ((> 3 3) 'greater)
#      ((< 3 3) 'less)
#      (else 'equal))""", "equal"),
#    ("""
#(cond (#f 1)
#      (#t 2)
#      (#t 3))""", '2'),
#    
#    ("(* 1 1)", '1'),
#    ("(* 5 7)", '35'),
#    ("(/ 1 1)", '1'),
#    ("(/ 1 2)", '1/2'),
#    ("(/ 42 2)", '21'),
#    
#    ("""
#(case (* 2 3)
#      ((2 3 5 7) 'prime)
#      ((1 4 6 8 9) 'composite))""", "composite"),
#    ("""
#(case (car '(c d))
#      ((a) 'a)
#      ((b) 'b))""", 'None'),
#    ("""
#(case (car '(c d))
#      ((a e i o u) 'vowel)
#      ((w y) 'semivowel)
#      (else 'consonant))""", "consonant"),
#    ('(quote (1 2 3))', "'(1 2 3)"),
#    ('"I am a string"', '"I am a string"'),
#    ('(string=? "I am a string" "I am a string")', '#t'),
#    ('(string=? "I am a string" "I am another string")', '#f'),
#    ('"\\""', '"\\""'),
#    ('" escapism \\" escapism"', '" escapism \\" escapism"'),
#    ('" esc \\\\ \\""', '" esc \\\\ \\""'),
#    ('(if (> 2 1) "2 > 1" "2 < 1")', '"2 > 1"'),
#    ('#\\a', '#\\a'),
#    ('#\\A', '#\\A'),
#    ('#\\(', '#\\('),
#    ('#\\space', '#\\space'),
#    ('(string #\\space)', '" "'),
#    ('(eq? (string #\\space) " ")', '#f'),
#    ('(eqv? (string #\\space) " ")', '#f'),
#    ('(equal? (string #\\space) " ")', '#t'),
#    
#    ("""
#(let ((x 1) (y 3))
#     x
#     y)""", '3'),
#    ("""
#(let ((x 1) (y 3))
#     y
#     x)""", '1'),
#    ("""
#(let ((x 1) (y 3))
#     (+ x y))""", '4'),
    
    ("""
((lambda (f a) (f f a))
 (lambda (self x)
  (cond
   ((= x 0) x)
   (else (+ x (self self (- x 1))))))
 5)""", '15'),
    
    ("""
((named-lambda (y f a) (f f a))
 (named-lambda (ff self x)
  (cond
   ((= x 0) x)
   (else (+ x (self self (- x 1))))))
 5)""", '15'),

    ("""
(%s 0)""" % (dragon,), '()'),

    ("""
(%s 1)""" % (dragon,), '(r)'),

    ("""
(%s 2)""" % (dragon,), '(r r l)'),

    ("""
(%s 3)""" % (dragon,), '(r r l r r l l)'),

    ("""
(%s 4)""" % (dragon,), '(r r l r r l l r r r l l r l l)'),

    ("""
(%s 7)""" % (dragon,), '(r r l r r l l r r r l l r l l r r r l r r l l l r r l l r l l r r r l r r l l r r r l l r l l l r r l r r l l l r r l l r l l r r r l r r l l r r r l l r l l r r r l r r l l l r r l l r l l l r r l r r l l r r r l l r l l l r r l r r l l l r r l l r l l)'),

    ("""
(%s 8)""" % (dragon,), '(r r l r r l l r r r l l r l l r r r l r r l l l r r l l r l l r r r l r r l l r r r l l r l l l r r l r r l l l r r l l r l l r r r l r r l l r r r l l r l l r r r l r r l l l r r l l r l l l r r l r r l l r r r l l r l l l r r l r r l l l r r l l r l l r r r l r r l l r r r l l r l l r r r l r r l l l r r l l r l l r r r l r r l l r r r l l r l l l r r l r r l l l r r l l r l l l r r l r r l l r r r l l r l l r r r l r r l l l r r l l r l l l r r l r r l l r r r l l r l l l r r l r r l l l r r l l r l l)'),

]

if __name__ == '__main__':
    verbose = len(sys.argv) > 1 and sys.argv[1] == '-v'

    for eval_func in [
#            'eval',
            'ceval'
    ]:
        for expression, expected in expressions:
        
            token = None
            result = None
            ex = None
            try:
                token = SchemeParser(expression).parse()
                s = Scheme(token)
                result = getattr(s, eval_func)()
                if str(result) != expected:
                     raise Exception("Test failed")
            except Exception, e:
                ex = e
        
            if verbose or ex:
                print "Input:    %s" % (expression,)
                print "Token:    %s" % (token,)
                print "Value:    %s" % (result,)
                print "Expected: %s" % (expected,)
                if ex:
                    if ex.args[0] == "Test failed":
                        print "Test failed"
                    else:
                        import sys
                        import traceback
                        traceback.print_exception(*sys.exc_info(), file=sys.stdout)
                print
