from llisp import Llisp, create_env, extend_env

env = {
        'print_a': print,
        'priny_b': lambda x: x*x*x,
        }

llisp = Llisp(extend_env(env))
llisp.repl()
