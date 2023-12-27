from http.server import HTTPServer, SimpleHTTPRequestHandler


class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        port = self.server.server_port
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = f"Hello from port {port}!"
        self.wfile.write(bytes(message, "utf8"))


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server_address = ("", port)

    httpd = HTTPServer(server_address, CustomRequestHandler)
    print(f"Server is listening on port {port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
