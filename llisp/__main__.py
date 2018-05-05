from llsip import Intepreter
import getopt, sys

def exec():
    if not sys.argv[1:]:
        usage()
        sys.exit(1)

    intepreter = Intepreter()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hit:', \
                ['help', 'interactive', 'target'])
        
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
            elif o in ('-i', '--interactive'):
                intepreter.repl()
            elif o in ('t', '--target'):
                intepreter.run(a)
            else:
                False, 'Unhandled arguments'
    except getopt.GetoptError as e:
        print(e)
                

def usage():
    print('Llisp --a python implemented lisp')
    print('')
    print('usage:')
    print('     python llisp [opts] <file>')
    print('')
    print('options:')
    print('     -h  --help')
    print('     -i  --interactive')
    print('     -t  --target <code path>')
                

if __name__ == '__main__':
    exec()
    
