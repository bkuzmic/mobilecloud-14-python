'''
Created on Jul 23, 2014

@author: bkuzmic
'''

import BaseHTTPServer
import cgi

HOST_NAME = 'localhost'
PORT_NUMBER = 8080

class Video:
    def __init__(self, name, url, duration):
        self.name = name
        self.url = url
        self.duration = duration
        
    def __repr__(self):
        return self.name + " : " + self.url
    
videoList = []

#video = Video("test","url",100)
#videoList.append(video)

class WebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self): 
        if not self.path.startswith("/video"):
            self.send_error(404, "Page Not Found")
            return
        
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()      
            
        for v in videoList:
            self.wfile.write(str(v) + "\n")
        
    def do_POST(self):
        if not self.path.startswith("/video"):
            self.send_error(404, "Page Not Found")
            return
        
        name = url = ''
        duration = -1
        
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
            
        #print postvars
        
        if postvars:
            name = postvars["name"][0]
            url = postvars["url"][0]
            try:
                duration = long(postvars["duration"][0])
            except ValueError:
                duration = -1
        
        if (name is None 
            or url is None 
            or duration < 0             
            or len(name.strip()) < 1
            or len(url.strip()) < 10):
            self.send_error(400, "Missing ['name','duration','url'].")
        else:
            video = Video(name, url, duration)
            videoList.append(video)
            self.wfile.write("Video added.")
            
        
    
if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), WebHandler)  
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()