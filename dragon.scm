 (lambda (f a) (f f a))
 (lambda (dragon i)
   (cond
    ((= i 0) '())
    (else
     ((lambda (f a c) (f f a c))
      (lambda (interp-rl d c)
        (cond
         ((null? d) '(r))
         ((= 1 (length d)) (cons c (rcons (if (equal? 'r c) 'l 'r) d)))
         (else
          (cons
           c
           (rcons
            (if (equal? 'r c) 'l 'r)
            (cons
             (car d)
             (rcons
              (rcar d)
              (interp-rl
               interp-rl
               (rcdr (cdr d))
               (if (equal? 'r c) 'l 'r)))))))))
      (dragon dragon (- i 1))
      'r))))
