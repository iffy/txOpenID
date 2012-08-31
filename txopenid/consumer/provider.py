# txopenid
# Copyright (c) 2007 Phil Christensen
#
# See LICENSE for details

"""
Provider information and access
"""



class Provider(object):
    """
    I am a collection of provider-specific data.
    
    @ivar discovery_url: URL to perform discovery on.
    
    @ivar endpoint: Endpoint URL
    """
    
    def __init__(self, discovery_url):
        self.discovery_url = discovery_url
        self.endpoint = None



class InMemoryProviderStore(object):
    """
    I hold L{Provider}s in memory.
    """
    
    
    def __init__(self):
        self.providers = {}
    
    
    def add(self, name, provider):
        """
        Store a L{Provider} under a C{name}.
        
        @param name: Name/key of provider.
        
        @type provider: L{Provider}
        
        @return: C{provider} passed in.
        """
        self.providers[name] = provider
        return provider


    def get(self, name):
        """
        Get a previously-stored L{Provider} by name/key.
        """
        return self.providers[name]


    def keys(self):
        """
        Get all the provider names/keys.
        
        @return: List of provider names.
        """
        return self.providers.keys()


    def items(self):
        return self.providers.items()


    def values(self):
        return self.providers.values()



