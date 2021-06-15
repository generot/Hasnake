import "stdlib.hs"

sieve (x : xs)  
	| empty(xs())	= [x()]
	| otherwise	= (x() : sieve(filteredLs()))
	where [ filteredLs = someFunc(x() xs()) ]

someFunc y ls = filter((\x -> mod(x()  y())) ls())

primes x = sieve([2..x()])
