from __future__ import print_function

import os
import sys
import random

from constants import *
from protocols.base import CommProtocol
    
class ModuloDHProtocol(CommProtocol):
    @classmethod
    def client_setup(cls, client, *args, **kwargs):
        setup_data = {}
        setup_data[PRIVATE_KEY] = cls.build_private_key(client=client)
        return setup_data
    
    @staticmethod
    def build_private_key(client, *args, **kwargs):
        key = client.pick_integer(*args, **kwargs)
        return key
        
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
        