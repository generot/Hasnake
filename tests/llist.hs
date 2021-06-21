makeLinkedList (x : xs)
	| empty(xs()) == 0 	= (x(), makeList(xs()))
	| otherwise		= x()

printLs ls depth
	| depth()	= printLn(fst(ls())) + printLs(snd(ls()) depth() - 1)
	| otherwise	= 0
