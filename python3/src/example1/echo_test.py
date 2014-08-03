
import unittest
import http.server
import threading, time
import echo

class TestVideoServer(unittest.TestCase):

    class ServerThread(threading.Thread):
        """Class used to start the server in the background while the tests are
        executed.
        """
        def run(self):
            self.httpd = http.server.HTTPServer(
                    ('localhost', 8080), echo.EchoHTTPRequestHandler)
            self.httpd.serve_forever()

        def stop(self):
            self.httpd.shutdown()

    @classmethod
    def setUpClass(cls):
        # Start the server on a separate thread and sleep for a tenth of a
        # second while it starts up
        cls.server = TestVideoServer.ServerThread()
        cls.server.start()
        time.sleep(.1)

    @classmethod
    def tearDownClass(cls):
        # Shut down the server once the tests are done
        cls.server.stop()

    def testMessageEchoing(self):
        message = '1234'
        url_encoded_params = '?msg=' + message

        connection = http.client.HTTPConnection('localhost:8080')
        connection.request('GET', '/echo' + url_encoded_params)

        response = connection.getresponse().read().decode()
        connection.close()

        self.assertEqual('Echo:' + message, response)

if __name__ == '__main__':
    unittest.main()

