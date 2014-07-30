'''
Created on Jul 30, 2014

@author: bkuzmic
'''

class NoDuplicatesVideoRepository(object):
    
    def __init__(self):
        self.videoSet = set()
        pass
    
    def addVideo(self, video):
        self.videoSet.add(video)
    
    def getVideos(self):
        return list(self.videoSet)
    
    def findByTitle(self, title):        
        foundSet = set()
        for v in self.videoSet:
            if v.name == title:
                foundSet.add(v)
        return list(foundSet)
    
class AllowDuplicatesVideoRepository(object):
    
    def __init__(self):
        self.videoSet = []
        pass
    
    def addVideo(self, video):
        self.videoSet.append(video)
    
    def getVideos(self):
        return self.videoSet
    
    def findByTitle(self, title):        
        foundSet = []
        for v in self.videoSet:
            if v.name == title:
                foundSet.append(v)
        return foundSet    