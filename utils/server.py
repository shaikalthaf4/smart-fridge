from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
DATABASE = 'utils/data/database.json'

class GP(BaseHTTPRequestHandler):
    def _set_headers(self, database_path=DATABASE):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.database_path = database_path
    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):
        self._set_headers()
        print(self.path)
        with open(self.database_path, "r") as fp:
            items = json.load(fp)
        self.wfile.write(bytes(json.dumps(items), encoding='utf-8'))
    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        print(form.getvalue("foo"))
        print(form.getvalue("bin"))
        self.wfile.write("<html><body><h1>POST Request Received!</h1></body></html>")

def run_server(IP_address, port):
    # ip address of the server, use ifconfig or ipconfig command to get ip
    # IP_address = '192.168.10.51'
    # port = 8080
    httpd = HTTPServer((IP_address, port), GP)
    httpd.serve_forever()