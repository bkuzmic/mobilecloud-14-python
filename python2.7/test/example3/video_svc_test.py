'''
Created on Jul 30, 2014

@author: bkuzmic
'''
import unittest
import json

from example3.video import Video
from example3.video_svc_api import VideoSvcApi
                 

class Test(unittest.TestCase):

    def testVideoSvcApi(self):
        video_svc = VideoSvcApi()

        v = Video(name="my video", url="http://my_video_url", duration=45)        
        result = video_svc.addVideo(v)
        self.assertTrue(result)
        
        videoList = video_svc.getVideoList()
        
        foundVideo = False
        for video in videoList:
            if video.name == v.name:
                foundVideo = True
               
        self.assertTrue(foundVideo)                   

        pass  


if __name__ == "__main__":
    unittest.main()