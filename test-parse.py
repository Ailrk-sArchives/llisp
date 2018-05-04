import llsip

code = '(define p 3) (print p)(define r 8) (print (* pi r))'
intepreter = llsip.Intepreter()

exp = intepreter.parse(code)
solution = intepreter.eval(intepreter.parse(code))
