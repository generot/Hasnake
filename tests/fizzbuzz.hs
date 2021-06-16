fizzbuzz n
	| mod(n() 15) == 0	= "FizzBuzz"
	| mod(n() 3) == 0	= "Fizz"
	| mod(n() 5) == 0	= "Buzz"
	| otherwise		= n()

fizzLs n = [fizzbuzz(x()) | x <- [1..n()]]
