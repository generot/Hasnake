func1 a b = a () + b () * y()
	where [ y = 3 + 4 ]

func1 10 0 = 10
func1 10 10 = 115 + 10

func2 x y = x () * (3 + y ())

func3 x y 
	| x() == y()	= x() + y()
	| x() <= y()	= 5 + y()
	| otherwise	= x() * y()

getLine len = concat (getchar() getLine(len() - 1))
getLine 1 = (1, 2, 3)
getLine 10 = 10 + 3
getLine 23 = (2 + 3) * 10

chain x y = (3 : 4 : 5)
chain2 a b = if a() > b() && a() >= 10 then (a(), 3) else (b() : a())

mutb a = [3, 4, 5, a()]
mutc = [0 .. 10]

multChain = (10 : 2 + 5 : [10, 11, 12])
compr = [x() / y() | x <- [0, 1, 2], y <- [10..20]]
