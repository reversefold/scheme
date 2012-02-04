(lambda (dragon i) (dragon dragon i))
 (lambda (dragon i)
   (cond
    ((= i 0) '())
    (else
     ((lambda (interp-rl c d) (interp-rl interp-rl c d))
      (lambda (interp-rl c d)
        (cons
         c
         (cond
          ((null? d) (list))
          (else
           (cons (car d) (interp-rl interp-rl (if (equal? c 'r) 'l 'r) (cdr d)))))))
      'r
      (dragon dragon (- i 1))))))
