length (x : xs)
	| empty(xs())	= 1
	| otherwise	= 1 + length(xs())

map lmb (x : xs)
	| empty(xs())	= [lmb(x())]
	| otherwise	= (lmb(x()) : map(lmb xs()))

filter lmb (x : xs)
	| empty(xs())	= if lmb(x()) then [x()] else []
	| lmb(x())	= (x() : filter(lmb xs()))
	| otherwise	= filter(lmb xs())

zip (x : xs) (y : ys)
	| empty(xs()) || empty(ys())	= [(x(), y())]
	| otherwise			= ((x(), y()) : zip(xs() ys()))

sum (x : xs)
	| empty(xs())	= x()
	| otherwise	= x() + sum(xs())

concat (x : xs) ls
	| empty(xs())	= (x() : ls())
	| otherwise	= (x() : concat(xs() ls()))

head (x : xs) = x()

tail (x : xs) = xs()
