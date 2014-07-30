'''
Created on Jul 30, 2014

@author: bkuzmic
'''

import json

class Video:
    
    def __init__(self, name="", url="", duration=0):
        self.name = name
        self.url = url
        self.duration = duration
    
    def __repr__(self):
        return json.dumps(self.__dict__)
        
    def fromJson(self, dict):       
        self.name = dict['name']
        self.url = dict['url']
        self.duration = dict['duration']
        