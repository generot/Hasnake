pascal x y
	| x() == y() || x() == 0 || y() == 0	= 1
	| otherwise				= if x() > y() 
						  then 0 
					  	  else pascal (x()  y() - 1) + pascal (x() - 1 y() - 1) 

pascalLine y = [if mod(pascal(x() y()) 2) then "*" else " " | x <- [0..y()]]
sierpinski y = [printLn(pascalLine (x())) | x <- [0..y()]]
