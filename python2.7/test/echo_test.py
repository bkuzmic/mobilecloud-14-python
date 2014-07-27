'''
Created on Jul 23, 2014

@author: boki
'''
import unittest
import httplib, urllib


class Test(unittest.TestCase):


    def testName(self):
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        conn.request("GET", "/echo?msg=1234")
        get_response = conn.getresponse()
        get_data = get_response.read()
        self.assertTrue("Echo:1234" in get_data)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()