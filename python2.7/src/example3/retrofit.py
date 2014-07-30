'''
Created on Jul 30, 2014

@author: bkuzmic
'''

import functools
import httplib
import json

import http_config

def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

class GET(object):
    
    def __init__(self, path, mapping_object=""):
        self.path = path        
        self.obj = mapping_object       
    
    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            conn = httplib.HTTPConnection(http_config.HOST + ":" + http_config.PORT)
            conn.request("GET", self.path)
            get_response = conn.getresponse()
            get_data = get_response.read()
            # get JSON data and convert it to dictionary            
            dict = json.loads(get_data)                
            list = []
            # get class of mapping object
            obj_class = get_class(self.obj)
        
            for d in dict:               
                # instantiate mapping object                
                t = obj_class()
                try:                
                    # populate each object from dictionary                    
                    t.fromJson(d)
                    list.append(t)
                except(KeyError):    
                    pass
            # return list of mapping objects as result    
            return list
           
        return decorated
    
class POST(object):
    
    def __init__(self, path):
        self.path = path               
    
    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            params = str(args[1])            
            headers = {"Content-type": "application/json", "Accept": "application/json"}
            conn = httplib.HTTPConnection(http_config.HOST + ":" + http_config.PORT)
            conn.request("POST", self.path, params, headers)
            response = conn.getresponse()            
            data = response.read() 
            dict = json.loads(data)
            if dict['status'] == "OK":
                return True                 
            else:
                return False
        return decorated