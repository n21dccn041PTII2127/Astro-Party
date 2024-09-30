class C(object):
    def __init__(self):
        self.c = 21
        self.__d = 42


class D(C):
    def __init__(self):
        self.e = 84
        C.__init__(self)


obj1 = D()
print(obj1.c)
print(obj1.__d)
