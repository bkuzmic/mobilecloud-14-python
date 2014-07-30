'''
Created on Jul 30, 2014

@author: bkuzmic
'''

from retrofit import GET, POST

class VideoSvcApi(object):
    '''
    This class defines an API for a VideoSvc. The
    interface is used to provide a contract for client/server
    interactions.
    '''

    def __init__(self):
        pass
    
    @GET("/video", mapping_object="example3.video.Video")
    def getVideoList(self):
        pass
    
    @POST("/video")
    def addVideo(self, video):
        pass
        