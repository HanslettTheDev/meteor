import errno
import io
import signal
import socket
import sys
import os

def grim_reaper(signum, frame):
    pid, status = os.waitpid(
        -1, # wait for any child process 
        os.WNOHANG # Do not block and return EWOULDBLOCK error
        )
    print(
        ' Child {pid} terminated with status {status}'
        '\n'.format(pid=pid, status=status)
    )

class WSGIServer(object):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5024

    def __init__(self, server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # bind
        listen_socket.bind(server_address)
        # activate
        listen_socket.listen(self.request_queue_size)
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.headers_set = []
    
    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        count = 0
        listen_socket = self.listen_socket
        while True:
            try:
                # new connection
                self.client_connection, client_address = listen_socket.accept()
                # handle one request and close the client connection and then
                # loop over to wait for another connection            except IOError as e:
            except IOError as e:    
                code, msg = e.args
                if code == errno.EINTR:
                    continue
                else:
                    raise
            pid = os.fork()
            if pid == 0:
                listen_socket.close()
                self.handle_one_request()
                os._exit(0)
            else:
                self.client_connection.close()
    
    def handle_one_request(self):
        request_data = self.client_connection.recv(1024)
        self.request_data = request_data =  request_data.decode('utf-8')

        # print formatted request data
        print("".join(f'< {line}\n' for line in request_data.splitlines()))
        self.parse_request(request_data)

        # Construct environment dictionary using reques  data
        env = self.get_environ()

        # Cal the application object to return an HTTP response body
        result = self.application(env, self.start_response)

        # construct a response and send back to the client
        self.finish_response(result)

    
    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        (self.request_method, self.path, self.request_version) = request_line.split()

    def get_environ(self):
        env = {}
         # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):
        # add necessar server headers
        server_headers = [
            ('Date', 'Mon 19 December 2022 5:54:48 GMT'),
            ('Server', 'WSGIServer 0.2')
        ]

        self.headers_set = [status, response_headers + server_headers]

        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = f'HTTP/1.1 {status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf8')
            # print formatted response data 
            print(''.join(
                f'> {line}\n' for line in response.splitlines()
            ))

            response_bytes = response.encode()
            self.client_connection.sendall(response_bytes)
        finally:
            self.client_connection.close()

SERVER_ADDRESS = (HOST, PORT) = '', 8080

def make_server(server_address, application):
    signal.signal(signal.SIGCHLD, grim_reaper)
    server = WSGIServer(server_address)
    server.set_app(application)
    return server

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callabl')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
    httpd.serve_forever()