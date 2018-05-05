from llisp import Llisp, extend_env, pylib_env_dict
import matplotlib.pyplot as plt
import numpy as np

llisp = Llisp(extend_env(pylib_env_dict(plt, np)))
llisp.repl()
