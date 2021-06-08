width = 14
scale = 9

coords sc = [(x() / sc(), -y() / sc()) | y <- [-width() / 2 .. width() / 2], x <- [-width() / 2 .. width() / 2]]
mandelFunc x y = (x() ^ 2 - y() ^ 2, 2 * x() * y())

iter x y cx cy it
	| it() < 20 && x() ^ 2 + y() ^ 2 < 4	= iter(fst(res()) + cx() snd(res()) + cy() cx() cy() it() + 1)
	| otherwise				= it()
	where [ res = mandelFunc(x() y()) ]

mset sc = [iter (fst(x()) snd(x()) fst(x()) snd(x()) 0) | x <- coords(sc())]
asterisks sc = [if x() == 20 then "*" else " " | x <- mset(sc())]

set ix (x : xs)
	| empty(xs())			= printLn(x())
	| mod(ix() width() + 1) == 0	= set(ix() + printLn("") xs())
	| otherwise			= set(ix() + print(x()) xs())

printSet scale = set(1 asterisks(scale()))
