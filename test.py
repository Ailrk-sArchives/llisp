from llisp import Llisp, extend_env, pylib_env_dict
import matplotlib.pyplot as plt
import numpy as np

env = pylib_env_dict(plt, np)
Llisp(extend_env(env)).repl()

