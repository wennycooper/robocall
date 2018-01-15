#!/usr/bin/env python
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE
# Written by Nathan Hamiel (2010)

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import urlparse
import os

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        parsed_path = urlparse.urlparse(self.path)
        #print(parsed_path)
        if parsed_path.path == "/robocall":
            #print("path matched!\n")
            d = urlparse.parse_qs(parsed_path.query)
            #print(d['roomId'][0])
            #print(parsed_path.query.roomId)
            #cmd = "echo kkuei | sudo -S asterisk -rx \"channel originate SIP/6001 extension 100@from-internal\""
            cmd = "echo kkuei | sudo -S asterisk -rx \"channel originate SIP/" + d['roomId'][0] + " extension 100@from-internal\""
            os.system(cmd)

        #print(request_path)
        #print(self.headers)
        print("<----- Request End -----\n")
        
        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        
    def do_POST(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print(request_path)
        
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        
        print(request_headers)
        print(self.rfile.read(length))
        print("<----- Request End -----\n")
        
        self.send_response(200)
    
    do_PUT = do_POST
    do_DELETE = do_GET
        
def main():
    port = 8080
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

        
if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
                    "Run:\n\n"
                    "   reflect")
    (options, args) = parser.parse_args()
    
    main()
