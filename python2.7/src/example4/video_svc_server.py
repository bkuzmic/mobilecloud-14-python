'''
Created on Jul 30, 2014

@author: bkuzmic
'''

import BaseHTTPServer

from urlparse import urlparse
import json
import urllib

import http_config
from video import Video
from video_repository import NoDuplicatesVideoRepository, AllowDuplicatesVideoRepository

HOST_NAME = http_config.HOST
PORT_NUMBER = int(http_config.PORT)

videoRepository = NoDuplicatesVideoRepository()


class WebHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self): 
        if not self.path.startswith("/video") and self.path.startswith("/video/find"):
            self.send_error(404, "Page Not Found")
            return
                
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers() 
        
        if self.path.startswith("/video/find"):
            self.findByTitle(self.path, self.wfile)
        else:
            self.getVideoList(self.wfile)                    
        
    def getVideoList(self, output):
        output.write(videoRepository.getVideos())
        
    def findByTitle(self, path, output):
        query = urlparse(self.path).query
        title = ""
        try:
            params = dict(qc.split("=") for qc in query.split("&"))
            title = urllib.unquote_plus(params["title"]).decode('utf8')             
        except ValueError:
            pass  
        output.write(videoRepository.findByTitle(title))        
        
    def do_POST(self):
        if not self.path.startswith("/video"):
            self.send_error(404, "Page Not Found")
            return        
        
        header = self.headers.getheader('content-type')              
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)            
        
        if header == "application/json":            
            dict = json.loads(post_body)
        else:
            self.send_error(400, "This server only accepts application/json POST data")         
        
        v = Video()
        try:                
            v.fromJson(dict)
            videoRepository.addVideo(v)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers() 
            self.wfile.write('{"status": "OK", "description": "Video added"}')
        except(KeyError):    
            self.send_error(400, "Missing ['name','duration','url'].")            
            
        
    
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), WebHandler)  
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()