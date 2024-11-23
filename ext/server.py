import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import serial

arduino = serial.Serial('COM3', 50000)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            value = int(float(post_data))
        except ValueError:
            value = 0

        if value < 0:
            value = 0
        elif value > 20:
            value = 20

        leds_on = value // 2
        print(post_data)
        arduino.write(str(leds_on).encode())
        
        # Send the response back to the client
        self._set_headers()
        self.wfile.write(f"Received and handled.".encode())

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument("-l", "--listen", default="localhost", help="Specify the IP address on which the server listens")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Specify the port on which the server listens")
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
