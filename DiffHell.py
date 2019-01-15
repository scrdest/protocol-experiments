from __future__ import print_function

import os
import sys
import random
        
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

PRIVATE_KEY = 'pr_key'
PUBLIC_KEY = 'pu_key'

DATA_SHARED = 'shared'

class CommProtocol(object):
    
    @classmethod
    def connect(cls, clients, *args, **kwargs):
        connection_data = {}
        connection_data.update(kwargs.get('data') or {})
        handshake_data = None
        
        max_handshake_attempts = kwargs.get('max_handshake_attempts', 1)
        handshake_attempts = 0
        
        while not handshake_data and handshake_attempts < max_handshake_attempts:
            handshake_attempts += 1
            try: handshake_data = cls.handshake(targets=clients, *args, **kwargs)
            except Exception as E: sys.excepthook(*sys.exc_info())
            
        if not handshake_data: raise Exception("Handshake could not be established after {att_num} attempts."
                                               .format(att_num=handshake_attempts)
                                               )
                                               
        connection_data[DATA_SHARED] = connection_data.get(DATA_SHARED) or {}
        connection_data[DATA_SHARED].update(handshake_data)
        
        for target in clients:
            if target not in connection_data:
                target_data = None
                
                try: target_data = cls.client_setup(client=target, **kwargs)
                except Exception as Exc: sys.excepthook(*sys.exc_info())
                
                if target_data: connection_data[target] = target_data
                                               
        return connection_data
        
        
    @classmethod
    def client_setup(cls, client, *args, **kwargs):
        """ """
        raise NotImplementedError
        
    @classmethod
    def handshake(cls, targets, *args, **kwargs):
        """ """
        raise NotImplementedError
    
    @staticmethod
    def build_private_key(*args, **kwargs):
        raise NotImplementedError
        
    
class ModuloDHProtocol(CommProtocol):
    @classmethod
    def client_setup(cls, client, *args, **kwargs):
        setup_data = {}
        setup_data[PRIVATE_KEY] = cls.build_private_key(client=client)
        return setup_data
    
    @staticmethod
    def build_private_key(client, *args, **kwargs):
        return client.pick_integer(*args, **kwargs)
        
    @classmethod
    def handshake(cls, targets, *args, **kwargs):
        handshake_data = {}
        
        pub_key = None
        pub_key = cls.build_public_key(clients=targets, **kwargs)
        
        if pub_key: handshake_data[PUBLIC_KEY] = pub_key
        
        
        
        return handshake_data
        
    @staticmethod
    def build_public_key(clients, *args, **kwargs):
        _clients = tuple(clients)
        prime = random.choice(_clients).pick_prime()
        root = random.choice(_clients).pick_primitive_root_mod(prime)      
        return (prime, root)
    
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
    runREPL(prompt=PROMPT, welcome_msg=HELLO_MSG, repl_globals=globals())
    
if __name__ == '__main__':
    main()