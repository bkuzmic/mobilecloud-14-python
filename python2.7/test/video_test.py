'''
Created on Jul 23, 2014

@author: boki
'''
import unittest
import httplib, urllib


class Test(unittest.TestCase):


    def testInsertVideo(self):
        params = urllib.urlencode({'name': 'Video - 1', 
                                   'url': 'http://coursera.org/some/video-1',
                                   'duration': 60 * 10 * 1000})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        conn.request("POST", "/video", params, headers)
        response = conn.getresponse()
        self.assertEqual(200, response.status, "Response status doesn't match")       
        data = response.read()
        self.assertTrue("Video added" in data) 
        
        conn.request("GET", "/video")
        get_response = conn.getresponse()
        get_data = get_response.read()
       
        self.assertTrue("Video - 1 : http://coursera.org/some/video-1" in get_data)
        
        conn.close()
                  
    
    def testMissingRequestParameter(self):
        params = urllib.urlencode({'name': '', 
                                   'url': 'http://coursera.org/some/video-1',
                                   'duration': 60 * 10 * 1000})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        conn.request("POST", "/video", params, headers)
        response = conn.getresponse()
        conn.close()
        self.assertEqual(400, response.status, "Response status doesn't match")
        self.assertTrue("Missing" in response.reason, "Wrong response reason")        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()