someFunc a b = a() + b() + y() - x()
	where [ y = a() * b() 
		x = a() - b() ]

func2 x y = x() * y()
func3 x = if x() > 0 then x() + func3(x() - 1) else 0

mult a b = a() * b()
func4 a b = a() + mult(a() b())
