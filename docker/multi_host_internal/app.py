from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = b"<h1>Internal Admin Panel</h1><p>Private network only.</p>"
            status_code = 200
        elif self.path == "/health":
            body = b"status=ok\nprofile=relay-cache\n"
            status_code = 200
        elif self.path == "/inventory":
            body = (
                b"service=internal admin\n"
                b"classification=private\n"
                b"relay_path=/relay/secret\n"
                b"relay_header=X-Relay-Key\n"
            )
            status_code = 200
        elif self.path == "/relay/secret":
            header = self.headers.get("X-Relay-Key", "")
            if header != "relay-stage-two":
                body = b"missing relay key"
                status_code = 403
            else:
                body = b"INTERNAL_DB_USER=legacy_admin\nINTERNAL_DB_PASS=P@ssw0rd-Internal\n"
                status_code = 200
        else:
            body = b"not found"
            status_code = 404

        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
