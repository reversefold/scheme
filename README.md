Scheme
======

A scheme parser and interpeter in python. There are two interpeter modes supported.

The first (eval) is the faster naive mode which recurses quite a bit and hence will hit the python recursion limit fairly quickly.

The second (ceval) uses a trampoline (continuation-passing-style) to continually pass control back up to the top of the stack and hence supports nearly infinite recursion. It's slower than the naive method, however, so the extra recursion comes at a cost.
