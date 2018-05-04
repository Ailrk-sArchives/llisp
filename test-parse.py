import llsip

code = '(define pi 3.1415) (define r 8) (print (* pi r))'
intepreter = llsip.Intepreter()

exp = intepreter.parse(code)
solution = intepreter.eval(intepreter.parse(code))
print(exp)
print(solution)
