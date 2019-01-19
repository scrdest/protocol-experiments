from __future__ import print_function

import os
import sys
import random

from protocols.diffhell import ModuloDHProtocol
        
PROMPT = 'DH> '
HELLO_MSG = """
    .--------------------------------------------.
    |                                            |
    |      SECURE PROTOCOL SIMULATOR 9001        |
    |                                            |
    '--------------------------------------------'
    
    Welcome!
    
    This environment is set up to simulate 
    the execution of secure key exchange protocols 
    between instances of abstract Agents.
    """

from constants import *
    
DEFAULT_AGENT_PROTOCOL = ModuloDHProtocol
    
class Agent(object):
    def __init__(self, protocol=None, *args, **kwargs):
        self.protocol = protocol or DEFAULT_AGENT_PROTOCOL
        self.connections = {}
        
    def __rshift__(self, other):
        return self.connect(other)
        
    def __lshift__(self, other):
        return self.request_connection(requester=other)
        
    @staticmethod
    def pick_integer(*args, **kwargs):
        return random.randint(1,300) # placeholder implementation
        
    @staticmethod
    def pick_prime(*args, **kwargs):
        return random.choice([3,5,7,11,13,17,19,23]) # placeholder implementation
        
    @staticmethod
    def pick_primitive_root_mod(*args, **kwargs):
        return random.choice([3,5,7,11,13,17,19,23]) # placeholder implementation
        
    def setup(self, target, protocol=None, **kwargs):
        _protocol = protocol or self.protocol
        setup_data = {target: {}}
        
        client_setup_data = None
        
        client_setup_data = _protocol.client_setup(client=self, target=target)
        setup_data[target].update(client_setup_data or {})
                
        return setup_data
        
    def connect(self, target, connection_data=None, protocol=None, **kwargs):
        _protocol = protocol or self.protocol
        _connection_data = connection_data or self.setup(target=target, protocol=_protocol)
        
        connection = None
        
        try: connection = _protocol.connect(clients={self, target}, data=_connection_data, **kwargs)
        except Exception as E: sys.excepthook(*sys.exc_info())
        
        if connection: self.connections[target] = connection
        return connection
    
    def request_connection(self, requester, **kwargs):
        connect_callsig = {}
        connect_callsig.update(kwargs)
        return self.connect(target=requester, **connect_callsig)
    
        
def main():
    global Agents
    Agents = {id(ag): ag for ag in (Agent() for _ in range(4))}
    
    global A,B
    A,B = [Agents[set(Agents).pop()] for _ in range(2)]
    
    from interfaces.cli import runREPL
    runREPL(prompt=PROMPT, welcome_msg=HELLO_MSG, repl_globals=globals(), repl_locals=locals())
    
if __name__ == '__main__':
    main()