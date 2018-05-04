import math, operator 
from typing import Union

#import pdb

class Exp(object):
    pass

""" Exp = (List, Atom)"""
class List(list, Exp):

    def __repr__(self):
        return '(List ' + \
        ''.join([str(self.__getitem__(i)) for i in range(0, self.__len__())]) + ') '

    def __str__(self):
        return '(List ' + \
        ''.join([str(self.__getitem__(i)) for i in range(0, self.__len__())]) + ') ' 

class Atom(Exp):
    val = None

    def __init__(self, value: Union[str, int, float]):
        self.val = value

    def __repr__(self):
       return  '<Atom ' + str(self.val) + '> '

    def __str__(self):
       return  '<Atom ' + str(self.val) + '> '


""" Atom = (Symbol, Number)"""
class Symbol(Atom):
    def __init__(self, value: str):
        super().__init__(value)

class Number(Atom):
    def __init__(self, value: Union[int, float]):
        super().__init__(value)


class Env(dict):
    """ 
    Env hold all language features 
    receive foo->dict to generate env
    """

    def __keytransform__(self, key):
        return str(key)

    def __init__(self, env_callback):
        self.update(env_callback())

    def __getitem__(self, key):
        return dict.__getitem__(self, self.__keytransform__(key))

    def __setitem__(self, key, value):
        return dict.__setitem__(self, self.__keytransform__(key), value)

    def __delitem__(self, key):
        return dict.__delitem__(self, self.__keytransform__(key))

    def __contains__(self, key):
        return dict.__contains__(self, self.__keytransform__(key))

class Intepreter():
    env = None

    def __init__(self, create_env_callback=None):
        if create_env_callback: self.env = Env(create_env_callback)
        else:                   self.env = Env(self.__create_default_env)

    def __create_default_env(self) -> dict:
        env = {}
        env.update(vars(math))
        env.update({
            '+': operator.add, '-': operator.sub,
            '*':operator.mul, '/':operator.truediv,
            '>':operator.gt, '<':operator.lt,
            '>=':operator.ge, '<=':operator.le, '=':operator.eq,
            'abs': abs,
            'append': operator.add,
            'begin': lambda *x: x[-1],
            'car':  lambda x: x[0],
            'cdr':  lambda x: x[1:],
            'cons': lambda x, y: [x] + y,
            'eq?':  operator.is_,
            'expt': pow,
            'equal?':   operator.eq,
            'length':   len,
            'list': lambda *x: List(x),
            'list?':lambda x: isinstance(x, List),
            'map':  map,
            'max':  max,
            'min':  min,
            'not':  operator.not_,
            'null?': lambda x: x==[],
            'number?': lambda x: isinstance(x, Number),
            'print': print,
            'procedure?': callable,
            'round': round,
            'symbol?': lambda x: isinstance(x, Symbol),
            })
        return env

    def __tokenizer(self, source_code: str) -> list:
        """ create a list of tokens """
        source_code = '(' + source_code + ')'
        return source_code.replace('(', ' ( ').replace(')', ' ) ').split()

    def parse(self, source_code: str) -> Exp:
        """ read Exp from tokens"""
        return self.__parse_parenthesis(self.__tokenizer(source_code))

    def __parse_parenthesis(self, tokens: list) ->Exp:
        """ parse one expression within parethesis """
        if len(tokens) == 0:
            raise SyntaxError('unexpected EOF')

        # get the top most token. pop out ( and ).
        token = tokens.pop(0)

        # generate a list
        if token == '(':
            expression = List()

            while tokens[0] != ')':
                expression.append(self.__parse_parenthesis(tokens))
            tokens.pop(0)
            return expression

        elif token == ')':
            raise SyntaxError(') mismatched')

        else:
            return Intepreter.atom(token)

    def eval(self, x: Exp) -> Exp:
        """ eval """
        # variable reference
        if isinstance(x, Symbol):
            return self.env[x.val]

        elif isinstance(x, Number):
            return x.val

        elif isinstance(x[0], Atom):

            elif x[0] == 'if':
                (_, test, conseq, alt) = x
                exp = (conseq if self.eval(test)  else alt)
                return self.eval(exp)

            elif x[0] == 'define':
                (_, symbol, exp) = x
                self.env[symbol] = eval(exp)


    @staticmethod
    def atom(token: str) -> Atom:
        """ method to transfer token from str to Number or Symbol """
        try:
            return Number(int(token))
        except ValueError:
            try:
                return Number(float(token))
            except ValueError:
                return Symbol(token)

