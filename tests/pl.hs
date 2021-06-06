import "../haslib/stdlib.hs"

ls = [0..10]
sq x = x() ^ 2

mappedLs = map(sq ls())
