'''
Created on Jul 30, 2014

@author: bkuzmic
'''
import unittest
import json

from example4.video import Video
from example4.video_svc_api import VideoSvcApi
                 

class Test(unittest.TestCase):
    
    def foundVideo(self, v, list):
        foundVideo = False
        for video in list:
            if video.name == v.name:
                foundVideo = True
        return foundVideo

    def testVideoSvcApi(self):
        video_svc = VideoSvcApi()            

        v = Video(name="my video", url="http://my_video_url", duration=45)        
        result = video_svc.addVideo(v)
        self.assertTrue(result)
        
        videoList = video_svc.getVideoList()    
               
        self.assertTrue(self.foundVideo(v, videoList))
        
        v = Video(name="test video", url="http://test_video_url", duration=20)        
        result = video_svc.addVideo(v)
        self.assertTrue(result)
        
        videoListByTitle = video_svc.findByTitle("test video")           
        
        self.assertTrue(self.foundVideo(v, videoListByTitle))    

        pass  


if __name__ == "__main__":
    unittest.main()