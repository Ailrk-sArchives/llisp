import math, operator , sys
from typing import Union

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
    def __repr__(self):
       return  '<Symbol ' + str(self.val) + '> '
    def __str__(self):
       return  '<Symbol ' + str(self.val) + '> '

class Number(Atom):
    def __init__(self, value: Union[int, float]):
        super().__init__(value)
    def __repr__(self):
       return  '<Numer ' + str(self.val) + '> '
    def __str__(self):
       return  '<Number ' + str(self.val) + '> '


class Env(dict):
    """ 
    Env hold all language features 
    receive foo->dict to generate env
    """

    def __keytransform__(self, key):
        return str(key)

    def __init__(self, parms=(), args=(), outer_env=None):
        self.update(zip(parms, args))
        self.outer_env = outer_env

    def find(self, var):
        # find from local scope to outer scope until reach global scope
        try:    
            return self if (var in self) else self.outer_env.find(var)
        except BaseException:
            print('unbounded item in all environments')
            sys.exit(1)

class Procedure(object):
    """ customizable procedure """

    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    
    # create a new Env with self.env as outer. bind self.parms with args for
    # the sub Env.

    # the  retur value is the parameters for Intepreter.eval to evaluate
    def __call__(self, *args):
        # create a new procedure, generate a local scope
        return self.body, Env(tuple(map(lambda x:x.val, self.parms)), args, self.env)

class Intepreter(object):
    env = None
    keywords = ['if', 'define', 'lambda', 'set!', 'quote']

    def __init__(self, create_global_env=None):
        if create_global_env:
            self.env = Env()
            self.env.update(create_global_env())
        else:
            self.env = Env()
            self.env.update(self.__create_std_global_env())

    def __create_std_global_env(self) -> dict:
        """ to create standard global env """
        env = {}
        env.update(vars(math))
        env.update({
            '+':            operator.add,
            '-':            operator.sub,
            '*':            operator.mul, 
            '/':            operator.truediv,
            '>':            operator.gt,
            '<':            operator.lt,
            '>=':           operator.ge,
            '<=':           operator.le,
            '=':            operator.eq,
            'abs':          abs,
            'append':       operator.add,
            'begin':        lambda *x: x[-1],
            'car':          lambda x: x[0],
            'cdr':          lambda x: x[1:],
            'cons':         lambda x, y: [x] + y,
            'eq?':          operator.is_,
            'expt':         pow,
            'equal?':       operator.eq,
            'length':       len,
            'list':         lambda *x: List(x),
            'list?':        lambda x: isinstance(x, List),
            'map':          map,
            'max':          max,
            'min':          min,
            'not':          operator.not_,
            'null?':        lambda x: x==[],
            'number?':      lambda x: isinstance(x, Number),
            'print':        print,
            'procedure?':   callable,
            'round':        round,
            'symbol?':      lambda x: isinstance(x, Symbol),
            })
        return env

    def __tokenizer(self, source_code: str) -> list:
        """ create a list of tokens """
        source_code = '(begin' + source_code + ')'
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

    def eval(self, x: Exp, env:Env=None) -> Exp:
        """ eval """
        # set env
        if not env: env = self.env

        # parse atom ===============
        # variable reference
        if isinstance(x, Symbol):
            try:
                return env.find(x.val)[x.val]
            except KeyError:
                print('Unbounded variable ' + x.val)
        
        # constant number
        elif not isinstance(x, List):
            return x.val

        # parse list =================
        op, *args = x
        if op.val == 'qoute':
            return args[0].val

        # condition
        elif op.val == 'if':
            (test, conseq, alt) = args
            exp = (conseq if self.eval(test, env)  else alt)
            return self.eval(exp, env)

        elif op.val == 'define':
            (symbol, exp) = args
            env[symbol.val] = self.eval(exp, env)

        elif op.val == 'set!':
            (symbol, exp) = args
            env.find(symbol.val)[symbol.val] = self.eval(exp, env)

        # generate procedure
        elif op.val == 'lambda':
            (parms, body) = args
            return Procedure(parms, body, env)

        # procedure call
        else:
            proc = self.eval(op, env)

            vals = List(self.eval(arg, env) for arg in args)
            
            # user defined procedures. proc(*vals) return the argument for eval
            if isinstance(self.env.find(op.val)[op.val], Procedure):
                sub_exp, sub_env = proc(*vals)
                return self.eval(sub_exp, sub_env)
            # build-in procedures
            return proc(*vals)

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
    
    def repl(self, prompt='>'):
        """ repl interactive shell"""
        while True:
            typein = input(prompt)
            if typein in ['q', 'exit', 'quit']: sys.exit(0)

            val = self.eval(self.parse(typein))
            if val:
                print(val)
