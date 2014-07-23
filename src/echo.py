'''
Created on Jul 23, 2014

@author: bkuzmic
'''

import BaseHTTPServer

from urlparse import urlparse

HOST_NAME = 'localhost'
PORT_NUMBER = 8080

class WebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self): 
        if not self.path.startswith("/echo"):
            self.notFound(self)
            return
        
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()      
            
        query = urlparse(self.path).query
        msg = ""
        try:
            params = dict(qc.split("=") for qc in query.split("&"))
            msg = params["msg"]
        except ValueError:
            msg = ""
                          
        self.wfile.write("Echo:" + msg)
    
    def notFound(self, s):
        s.send_response(404)
        s.send_header("Content-type", "text/plain")
        s.end_headers()  
        s.wfile.write("404 - Page Not Found")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), WebHandler)  
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()    