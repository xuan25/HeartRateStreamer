from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import socket

try:
    from osc_controller import send_heart_rate
except ImportError:
    print("Warning: OSC controller not available. Heart rate will not be sent to OSC.")

    def send_heart_rate(heart_rate, timestamp=None):
        _, _ = heart_rate, timestamp

SERVER_PORT = 8000

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_response(self):

        self.send_response(200)
        self.end_headers()

    # @override
    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        payload = json.loads(post_data.decode('utf-8'))

        self._set_response()

        logging.info(payload)

        # Send heart rate to OSC
        send_heart_rate(payload["heartRate"], payload["timestamp"])

def main():
    logging.basicConfig(level=logging.INFO)

    logging.info('Starting HTTP server...')

    ip_addresses = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]
    logging.info('IP addresses: %s', ip_addresses)
    logging.info('Server port: %d', SERVER_PORT)
    
    server_address = ('', SERVER_PORT)
    http_server = HTTPServer(server_address, HTTPRequestHandler)

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        pass

    logging.info('Stopping HTTP server...')
    http_server.server_close()

    # reset OSC heart rate
    send_heart_rate(0.0)

if __name__ == '__main__':
    main()
