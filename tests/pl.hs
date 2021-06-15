import "../haslib/stdlib.hs"

ls = [0..10]
sq x = x() ^ 2

lmb a b c = (\x y -> x() + y())

mappedLs = map(sq ls())
evenNums = filter(check ls())

factorial x
	| x() == 0	= 1
	| otherwise	= x() * factorial(x() - 1)

fib a
	| a() < 2	= a()
	| otherwise	= fib(a() - 1) + fib(a() - 2)
