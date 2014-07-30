'''
Created on Jul 30, 2014

@author: bkuzmic
'''

import BaseHTTPServer

import json

import http_config
from video import Video

HOST_NAME = http_config.HOST
PORT_NUMBER = int(http_config.PORT)

videoList = []


class WebHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self): 
        if not self.path.startswith("/video"):
            self.send_error(404, "Page Not Found")
            return
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()      
                    
        self.wfile.write(videoList)
        
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
            videoList.append(v)
            
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