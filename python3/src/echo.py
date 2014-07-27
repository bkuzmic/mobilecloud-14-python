
""" Python example of a simple web server that looks for a single query
parameter on an HTTP request and echoes that parameter back to the client in
the HTTP response.
"""

# Check https://docs.python.org/3/library/http.server.html
# and https://docs.python.org/3.4/library/urllib.parse.html
# for more information on these modules
import http.server
import urllib.parse

class EchoHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """ Class to handle the HTTP requests coming to the server. """

    def do_GET(self):
        """ Handle GET requests returning the msg query parameter. """
        # Every GET request is routed to this function. Here we make sure the
        # client gets a 404 for any resource different from '/echo'
        urlparse_tuple = urllib.parse.urlparse(self.path)
        if urlparse_tuple.path != '/echo':
            self.send_error(404)    # Providing an error message is optional,
                                    # python has default messages for each code
            return

        try:
            # Try to parse the query parameters to get msg
            url_query = urlparse_tuple.query
            query_parameters = urllib.parse.parse_qs(url_query)
            msg = query_parameters['msg'][0]
        except KeyError:
            # Default to the empty string if the parameter msg wasn't provided
            msg = ''

        # Fill the HTTP response status line and headers
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Strings in python 3 are unicode characters. In order to write them
        # out on a buffer you need to encode them first. Check:
        # https://docs.python.org/3/howto/unicode.html#the-string-type
        # https://docs.python.org/3/howto/unicode.html#converting-to-bytes
        self.wfile.write(('Echo:' + msg).encode())


if __name__ == "__main__":
    SERVER_ADDRESS = ("localhost", 8080)

    # The constructor of HTTPServer receives a tuple containing the server's
    # address and port, and a RequestHandlerClass to which the HTTP requests
    # will be routed
    server = http.server.HTTPServer(SERVER_ADDRESS, EchoHTTPRequestHandler)

    try:
        print('serving..')
        server.serve_forever()
    except KeyboardInterrupt:
        print('..interrupted')

    server.server_close()

