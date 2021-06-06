import "../haslib/stdlib.hs"

ls = [0..10]
sq x = x() ^ 2

check a = mod(a() 2) == 0

mappedLs = map(sq ls())
evenNums = filter(check ls())
