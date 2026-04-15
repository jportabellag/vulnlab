from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/secret":
            body = b"INTERNAL_TOKEN=netops-local-only\nDEBUG_PORTAL=http://127.0.0.1:9000/metrics\n"
        elif self.path == "/metrics":
            body = b"requests=42\nbackend=inventory-api\n"
        else:
            body = b"internal service\n"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


HTTPServer(("127.0.0.1", 9000), Handler).serve_forever()
