from typing import Union

class Exp(object):
    pass

""" Exp = (List, Atom)"""
class List(list, Exp):

    def __repr__(self):
        return '(List ' + \
        ''.join([str(self.__getitem__(i)) for i in range(0, self.__len__())]) + ') '

    __str__ = __repr__

class Atom(Exp):
    val = None
    def __init__(self, value: Union[str, int, float]):
        self.val = value

    def __repr__(self):
       return  '<Atom ' + str(self.val) + '> '

    __str__ = __repr__

""" Atom = (Symbol, Number)"""
class Symbol(Atom):
    def __init__(self, value: str):
        super().__init__(value)

    def __repr__(self):
       return  '<Symbol ' + str(self.val) + '> '
    
    __str__ = __repr__

class Number(Atom):
    def __init__(self, value: Union[int, float]):
        super().__init__(value)
    def __repr__(self):
       return  '<Numer ' + str(self.val) + '> '

    __str__ = __repr__

