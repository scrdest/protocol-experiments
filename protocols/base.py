from constants import *

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