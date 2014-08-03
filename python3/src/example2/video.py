
"""Python example of a web server that keeps an in-memory list of videos.
The server allows for videos to be added with POST requests, and clients can
have access to the list of videos itself through a GET request.
"""

# Check https://docs.python.org/3/library/http.server.html
# https://docs.python.org/3.4/library/urllib.parse.html
# https://docs.python.org/3/library/cgi.html
# for more information on these modules
import http.server
import urllib.parse
import cgi


class Video:
    """Data representation class for videos."""
    def __init__(self, name, url, duration):
        self.name = name
        self.url = url
        self.duration = duration

    def __repr__(self):
        return self.name + ' : ' + self.url

    def encode(self):
        return (self.__repr__() + '\n').encode()


class VideoHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Class to handle the HTTP requests coming to the server."""

    # In-memory list of videos added to the server
    videos = []

    def request_parameters(self):
        """Return a dictionary with parameters from both the URL query string
        and the url encoded form body.
        """
        request_parameters = {}

        # Get the parameters from the request body
        content_type, _ = cgi.parse_header(self.headers['content-type'])

        if content_type == 'application/x-www-form-urlencoded':
            content_length = int(self.headers['content-length'])
            body_parameters = urllib.parse.parse_qs(
                    self.rfile.read(content_length))

            request_parameters.update(body_parameters)

        # Get the parameters from the query string
        urlparse_tuple = urllib.parse.urlparse(self.path)
        url_query = urlparse_tuple.query
        query_parameters = urllib.parse.parse_qs(url_query)

        request_parameters.update(query_parameters)

        # Turn the keys and values of the result dictionary into normal python
        # strings
        for k in request_parameters.keys():
            param = request_parameters[k][0]
            if type(param) is bytes:
                param = param.decode()
            if type(k) is bytes:
                key = k.decode()
                del request_parameters[k]
                k = key

            request_parameters[k] = param

        return request_parameters

    class VideoHandler:
        """Class to handle the HTTP requests to the resource /video."""
        @staticmethod
        def do_GET(handler):
            """Handle GET requests to /video."""
            # Fill the HTTP response with the appropriate headers
            handler.send_response(200)
            handler.send_header('Content-type', 'text/plain')
            handler.end_headers()

            # Write out the information of the videos
            for video in VideoHTTPRequestHandler.videos:
                handler.wfile.write(video.encode())

        @staticmethod
        def do_POST(handler):
            """Handle POST requests to /video."""
            # Get a dictionary with the HTTP request parameters
            request_parameters = handler.request_parameters()

            name, url, duration = '', '', -1

            try:
                name = request_parameters['name'].strip()
                url = request_parameters['url'].strip()
                duration = int(request_parameters['duration'])
            except:
                pass

            # Validate whether the necessary parameters were correctly provided
            if len(name) == 0 or len(url) < 10 or duration <= 0:
                handler.send_error(400, "Missing ['name','duration','url'].")
            else:
                # With the validated data we can commit the new video to memory
                video = Video(name, url, duration)
                VideoHTTPRequestHandler.videos.append(video)

                # Send back the appropriate response
                handler.send_response(200)
                handler.send_header('Content-type', 'text/plain')
                handler.end_headers()
                handler.wfile.write('Video added.'.encode())


    class HTMLVideoHandler:
        """Class to handle the HTTP requests to the resource /view/video."""
        @staticmethod
        def do_GET(handler):
            """Handle GET requests to /view/video."""
            # Fill the response header
            handler.send_response(200)
            handler.send_header('Content-type', 'text/html')
            handler.end_headers()

            # Provide a form to make it easier doing POST requests
            ui_form = ("<form name='formvideo' method='POST' target='_self'>" +
                    "<fieldset><legend>Video Data</legend>" +
                    "<table><tr>" +
                    "<td><label for='name'>Name:&nbsp;</label></td>" +
                    "<td><input type='text' name='name' id='name' size='64' " +
                        "maxlength='64' /></td>" +
                    "</tr><tr>" +
                    "<td><label for='url'>URL:&nbsp;</label></td>" +
                    "<td><input type='text' name='url' id='url' size='64' " +
                        "maxlength='256' /></td>" +
                    "</tr><tr>" +
                    "<td><label for='duration'>Duration:&nbsp;</label></td>" +
                    "<td><input type='text' name='duration' id='duration' " +
                        "size='16' maxlength='16' /></td>" +
                    "</tr><tr>" +
                    "<td style='text-align: right;' colspan=2><input " +
                        "type='submit' value='Add Video' /></td>" +
                    "</tr></table></fieldset></form>")
            handler.wfile.write(ui_form.encode())

            # Print out the videos saved in the server
            for video in VideoHTTPRequestHandler.videos:
                handler.wfile.write(video.encode())

        @staticmethod
        def do_POST(handler):
            """Handle POST requests to /view/video."""
            # Get a dictionary with the HTTP request parameters
            request_parameters = handler.request_parameters()

            name, url, duration = '', '', -1

            try:
                name = request_parameters['name'].strip()
                url = request_parameters['url'].strip()
                duration = int(request_parameters['duration'])
            except:
                pass

            # Validate whether the necessary parameters were correctly provided
            if len(name) == 0 or len(url) < 10 or duration <= 0:
                handler.send_error(400, "Missing ['name','duration','url'].")
            else:
                # With the validated data we can commit the new video to memory
                video = Video(name, url, duration)
                VideoHTTPRequestHandler.videos.append(video)

                # Return the user to the page with the form
                VideoHTTPRequestHandler.HTMLVideoHandler.do_GET(handler)

    def do_GET(self):
        """Handle every GET request directed to the server."""
        # Make sure the client gets a 404 for any resource different from
        # '/video' or '/view/video'.
        urlparse_tuple = urllib.parse.urlparse(self.path)

        # Route '/video' to VideoHandler
        if urlparse_tuple.path == '/video':
            VideoHTTPRequestHandler.VideoHandler.do_GET(self)
        # Route '/view/video' to HTMLVideoHandler
        elif urlparse_tuple.path == '/view/video':
            VideoHTTPRequestHandler.HTMLVideoHandler.do_GET(self)
        else:
            self.send_error(404)

    def do_POST(self):
        """Handle every POST request directed to the server."""
        # Sends 404 for any resource different from '/video' or '/view/video'
        urlparse_tuple = urllib.parse.urlparse(self.path)

        # Route '/video' to VideoHandler
        if urlparse_tuple.path == '/video':
            VideoHTTPRequestHandler.VideoHandler.do_POST(self)
        # Route '/view/video' to HTMLVideoHandler
        elif urlparse_tuple.path == '/view/video':
            VideoHTTPRequestHandler.HTMLVideoHandler.do_POST(self)
        else:
            self.send_error(404)


if __name__ == "__main__":
    SERVER_ADDRESS = ("localhost", 8080)

    # The constructor of HTTPServer receives a tuple containing the server's
    # address and port, and a RequestHandlerClass to which the HTTP requests
    # will be routed
    server = http.server.HTTPServer(SERVER_ADDRESS, VideoHTTPRequestHandler)

    try:
        print('serving..')
        server.serve_forever()
    except KeyboardInterrupt:
        print('..interrupted')

    server.shutdown()


