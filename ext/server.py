from http.server import HTTPServer, BaseHTTPRequestHandler
import serial

# Open a serial connection to Arduino
arduino = serial.Serial('COM3', 50000)  # Adjust COM port as needed

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        print(f"Received POST data: {post_data}")

        try:
            value = int(float(post_data))
        except ValueError:
            value = 0
            print("Invalid value received, defaulting to 0.")
        
        if value < 0:
            value = 0
        elif value > 20:
            value = 20

        leds_on = value // 2 
        arduino.write(str(leds_on).encode())

        self._set_headers()
        self.wfile.write(f"POST request handled! {leds_on} LEDs are now ON.".encode())

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

def run(addr="127.0.0.1", port=8000):
    server_address = (addr, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Serving on http://{addr}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
