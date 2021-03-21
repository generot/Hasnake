class Iterator:
    def __init__(self, ls):
        self.iter = self.iterator(ls)
        self.curr = self.gnext(self.iter)

    def next(self):
        self.curr = self.gnext(self.iter)

    @staticmethod
    def iterator(arr):
        for i in arr:
            yield(i)

    @staticmethod
    def gnext(_iterator):
        try:
            return str(next(_iterator))
        except StopIteration:
            return ""

def CheckToken(itr, *args):
    for i in args:
        if itr.curr == i:
            return True

    return False
