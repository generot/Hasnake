someFunc a b = a() + b() + y() - x()
	where [ y = a() * b() 
		x = a() - b() ]

func2 x y = x() * y()
func3 x = if x() > 0 then x() + func3(x() - 1) else 0

mult a b = a() * b()
func4 a b = a() + mult(a() b())

guarded x
	| x() > 0	= "Bigger than 0"
	| x() < 0	= "Less than 0"
	| otherwise	= "Is 0"

fibonacci a
	| a() < 2	= a()
	| otherwise	= fibonacci(a() - 1) + fibonacci(a() - 2)

chainFunc lim
	| lim() > 0	= (mult(lim() 2) : chainFunc(lim() - 1))
	| otherwise	= []

getLambda lmb a b = lmb(a() b()) + a()
head a (x : xs) = x() + a()

length (x : xs)
	| empty(xs()) == 1	= 1
	| otherwise		= 1 + length(xs())

moreDest (x : y : xs) = x() + y()

sq a = a() * a()

map lmb (x : xs)
	| empty(xs()) == 1	= [lmb(x())]
	| otherwise		= (lmb(x()) : map(lmb xs()))
