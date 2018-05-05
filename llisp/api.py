from .llsip import Env
from types import FunctionType
import operator


def create_env(env: dict) -> FunctionType:
    """ return a higher order funtion to generate dict """
    def foo() -> dict:
        env.update({
            'begin':        lambda *x: x[-1],
            'print':        print,
            })
        return env
    return foo

def extend_env(env: dict) -> FunctionType:
    """ return a env with standard env as subset """
    def foo() -> dict:
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
    return foo

def pylib_env_dict(*args) -> dict:
    """ return a dict of given libs """
    env = {}
    for lib in args:
        env.update(vars(lib))
    return env
