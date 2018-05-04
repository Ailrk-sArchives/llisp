import llsip

code = '(define r 10)  (print (* pi (* r r)))'

intepreter = llsip.Intepreter()

intepreter.repl()
