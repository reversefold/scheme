(lambda (mergesort fh lh l) (mergesort mergesort fh lh l))
 (lambda (mergesort fh lf l)
   (cond
    ((< (length l) 2) l)
    (else
     ((lambda (mergesorted l1 l2) (mergesorted mergesorted l1 l2))
      (lambda (mergesorted l1 l2)
        (cond
         ((= (length l1) 0) l2)
         ((= (length l2) 0) l1)
         ((< (car l1) (car l2))
          (cons (car l1) (mergesorted mergesorted (cdr l1) l2)))
         (else
          (cons (car l2) (mergesorted mergesorted l1 (cdr l2))))))
      (mergesort mergesort fh lh (fh l))
      (mergesort mergesort fh lh (lh l))))))
 (lambda (l)
   ((lambda (fhi l n) (fhi fhi l n))
    (lambda (fhi l n)
      (cond
       ((= n 0) '())
       (else (cons (car l) (fhi fhi (cdr l) (- n 1))))))
    l
    (ceiling (/ (length l) 2))))
 (lambda (l)
   ((lambda (lhi l n) (lhi lhi l n))
    (lambda (lhi l n)
      (cond
       ((= n 0) l)
       (else
        (lhi lhi (cdr l) (- n 1)))))
    l
    (- (length l) (floor (/ (length l) 2)))))
