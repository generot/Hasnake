PI = 3.14159265359

factorial n
	| n() == 0	= 1
	| otherwise	= n() * factorial(n() - 1)

sum n = if n() /= 0 then n() + sum(n() - 1) else 0
gaussSum n = n() * (n() + 1) / 2

deg a = a() * 180 / PI()
rad a = a() * PI() / 180

sin a = a() - a() ^ 3 / factorial(3) + a() ^ 5 / factorial(5) - a() ^ 7 / factorial(7)
cos a = (1 - sin(a()) ^ 2) ^ 0.5
tan a = sin(a()) / cos(a())
cotg a = 1 / tan(a())
