from __future__ import print_function

import os
import sys
from pprint import pprint

PRINTER = 'current_printer'

def switch_pprint(curr_state):
    state = curr_state.copy()
    curr_printer = state.get(PRINTER)
    new_printer = pprint if curr_printer is not pprint else print
    print('Pretty Printing {}'.format('enabled' if new_printer is pprint else 'disabled'))
    state[PRINTER] = new_printer
    return state
    

REPL_SPECIAL_COMMANDS = {
    '>PP': switch_pprint
}    
        
def runREPL(prompt= '> ', welcome_msg='', repl_globals=None):
    if repl_globals: globals().update(repl_globals)
    config = {}
    config[PRINTER] = print
    
    run_loop = True
    print(welcome_msg)
    
    while run_loop:
        try: 
            user_input = input(prompt)
            special_input_handler = REPL_SPECIAL_COMMANDS.get(user_input.upper(), NotImplemented)
            
            if special_input_handler is NotImplemented:
                try: config[PRINTER](repr(eval(user_input)))
                except SyntaxError: exec(user_input)
                
            else:
                config.update(special_input_handler(config))
            
        except (EOFError, KeyboardInterrupt): run_loop = False
        except Exception: sys.excepthook(*sys.exc_info())
    
    else:
        print('Quitting...')
    
        
def main():
    runREPL()
    
if __name__ == '__main__':
    main()