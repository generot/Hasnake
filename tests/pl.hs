import "../haslib/stdlib.hs"

ls = [0..10]
sq x = x() ^ 2

lmb a b c = (\x y -> x() + y())

mappedLs = map(sq ls())
evenNums = filter(check ls())
