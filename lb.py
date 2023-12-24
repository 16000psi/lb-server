from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header("Content-type", "text/html")
        self.end_headers()

        message = f"Received request at path: {self.path}"
        self.wfile.write(bytes(message, "utf8"))
        print(message)
        print(self.requestline)
        for header in self.headers:
            print(f"{header}: {self.headers[header]}")



def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=999):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Server is listening on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
