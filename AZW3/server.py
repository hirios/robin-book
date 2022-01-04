import http.server
import socketserver


# If you want to make the download list available


PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("ON LOCALHOST - PORT: ", PORT)
    httpd.serve_forever()
