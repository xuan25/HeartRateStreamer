from pythonosc.udp_client import SimpleUDPClient

OSC_IP = "127.0.0.1"
OCS_PORT = 9000

class HeartRateOSCSender:

    def __init__(self, ip, port):
        self.client = SimpleUDPClient(ip, port)
        self.last_timestamp = 0

    def send_heart_rate(self, heart_rate, timestamp=None):
        if timestamp is None or timestamp > self.last_timestamp:
            self.client.send_message("/avatar/parameters/HR", heart_rate)
            self.last_timestamp = timestamp
