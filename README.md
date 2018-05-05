# LLisp a scheme toy language

### Another scheme dialect. Partially support scheme's basic functionality, while provide a extendable interface for customizable environment. 

## features

* Support lambda expression.
* Provide a repl shell.
* Provide application interface for customized built-in functions.

## how to use

- import customized environment to llist

```python
# this is your program
from llisp import Llisp, extend_env
from os import environ
import sys

# write your own env in form of dictionary
env = {
    'exit':	 sys.exit
}

env.update(environ)

llisp = Llisp(extend_env(env))
llisp.repl()
```



- import python library into llisp environment

```python
# this is your program
from llisp import Llisp, extend_env, pylib_env_dict
import matplotlib.pyplot as plt
import numpy as np

# write your own env in form of dictionary

env = pylib_env_dict(plt, np)

llisp = Llisp(extend_env(env))
llisp.repl()
```



