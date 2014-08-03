
import unittest
import http.server, http.client, urllib.parse
import threading, time, random
import video

class TestVideoServer(unittest.TestCase):

    class ServerThread(threading.Thread):
        """Class used to start the server in the background while the tests are
        executed.
        """
        def run(self):
            self.httpd = http.server.HTTPServer(
                    ('localhost', 8080), video.VideoHTTPRequestHandler)
            self.httpd.serve_forever()

        def stop(self):
            self.httpd.shutdown()

    @classmethod
    def setUpClass(cls):
        # Start the server on a separate thread and sleep for one second while
        # it starts up
        cls.server = TestVideoServer.ServerThread()
        cls.server.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        # Shut down the server once the tests are done
        cls.server.stop()

    @staticmethod
    def executeVideoHTTPRequest(request_type='GET', name=None, url=None,
            duration=None):
        """Execute an HTTP request to /video, returning its HTTPConnection."""
        body = None
        headers = {}

        if request_type == 'POST':
            # Represent the video data in a dictionary
            data = {'name': name, 'url': url, 'duration': duration}
            # Parse the video data from the dictionary into a URL encoded string
            body = urllib.parse.urlencode(data)
            # Set the correct content-type for the request
            headers = {'content-type': 'application/x-www-form-urlencoded'}

        # Make HTTP request
        connection = http.client.HTTPConnection('localhost:8080')
        connection.request(request_type, '/video', body=body, headers=headers)

        return connection

    def testVideoAddAndList(self):
        """Test if a video can be successfully added to the server."""
        # Generate a random ID for the video each time the test is executed
        randomID = str(random.randint(0, 10**3))
        # Initialize video creation parameters
        name = 'Video - ' + randomID
        url = 'http://coursera.org/some/video-' + randomID
        duration = 60 * 10 * 1000

        # Get HTTPConnection for the POST request
        connection = self.executeVideoHTTPRequest('POST', name, url, duration)

        httpResponse = connection.getresponse()
        responseBody = httpResponse.read().decode()
        connection.close()

        # Assert request was successful
        self.assertEqual(200, httpResponse.getcode())

        # Assert the response body has the expected content
        self.assertEqual('Video added.', responseBody)

        connection = self.executeVideoHTTPRequest()
        responseBody = connection.getresponse().read().decode().strip()
        returnedVideos = responseBody.split('\n')

        # Assert the inserted video is in the returned list of videos
        expectedVideoDescription = name + ' : ' + url
        self.assertTrue(expectedVideoDescription in returnedVideos)

    def testMissingRequestParameter(self):
        # Generate a random ID for the video each time the test is executed
        randomID = str(random.randint(0, 10**3))
        # Initialize video creation parameters with empty name
        name = ''
        url = 'http://coursera.org/some/video-' + randomID
        duration = 60 * 10 * 1000

        # Get HTTPConnection for the POST request
        connection = self.executeVideoHTTPRequest('POST', name, url, duration)

        httpResponse = connection.getresponse()

        # Assert server returns a 400 bad request
        self.assertEqual(400, httpResponse.getcode())

if __name__ == '__main__':
    unittest.main()

