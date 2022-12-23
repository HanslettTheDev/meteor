# from flask import Flask
# from flask import Response

# app = Flask('flaskapp')

# @app.route("/home")
# def home():
#     return Response(
#         'Hello world from flask \n',
#         mimetype='text/plain'
#     )

# apps = app.wsgi_app

# def app(environ, start_response):
#     '''A barebones WSGI application
#     This is the starting point for your own web framework
#     '''

#     print(environ)
#     status = '200 OK'
#     response_headers = [('Content-Type', 'text/plain; charset=utf8')]
#     start_response(status, response_headers) #callback function
#     return [b'Hello world from a simple WSGI application!\n']

def app(environ, start_response):
	print(environ)
	data = b"Hello, World!\n"
	start_response("200 OK", [
		("Content-Type", "text/plain"),
		("Content-Length", str(len(data)))
	])
	return iter([data])



