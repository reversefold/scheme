(lambda (dragon rcons i) (dragon dragon rcons i))
 (lambda (dragon rcons i)
   (cond
    ((= i 0) '())
    (else
     ((lambda (interp-rl rcons d c) (interp-rl interp-rl rcons d c))
      (lambda (interp-rl rcons d c)
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
              ((lambda (f a) (f f a)) (lambda (rcar l) (cond ((= 1 (length l)) (car l)) (else (rcar rcar (cdr l))))) d)
              (interp-rl
               interp-rl
               rcons
               ((lambda (f a) (f f a)) (lambda (rcdr l) (cond ((= 1 (length l)) '()) (else (cons (car l) (rcdr rcdr (cdr l)))))) (cdr d))
               (if (equal? 'r c) 'l 'r)))))))))
      rcons
      (dragon dragon rcons (- i 1))
      'r))))
 (lambda (v l) ((lambda (rcons v l) (rcons rcons v l)) (lambda (rcons v l) (cond ((null? l) (list v)) (else (cons (car l) (rcons rcons v (cdr l)))))) v l))
