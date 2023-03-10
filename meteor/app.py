from .serve import Response, Request
from .router import Router

class Meteor:
	def __init__(self):
		self.routes = dict()
	
	def __call__(self, environ, start_response):
		'''Overide the default call function so it can automatically add all routes to the context'''
		# A normal wsgi setup exposing an application callable and returning an iter object
		# The self.handle_request does one thing. Get the call back function from the routes decorator
		# that was added to the dictionary and return it as the response object
		request = Request(environ)
		response: Response = self.handle_request(request)
		# try:
		start_response(response.status, response.headers.items())
		# except AttributeError:
		# 	return iter(Response(["Favicon not found"], 404))
		return iter(response)
	
	def error_response(self, response: Response):
		response.status_code = 404
		response.response = ["<h1 style='text-align: center;'>Sorry!, Page not found</h1>"]

	def route(self, path):
		# A decorater which recieves a path variable and adds them to the function handler
		def wrapper(function_handler):
			self.routes[path] = function_handler
			return function_handler
		return wrapper
	
	def get_handler(self, request: Request):
		for path, handler in self.routes.items():
			router = Router(path, request.path)
			url = router.start() 
			if request.path == url:
				if router.hasVar:
					return handler(request, *router.vars)
				return handler(request)
		
		return None
	
	def handle_request(self, request: Request):
		response = Response()
		
		handler = self.get_handler(request)
		if handler:
			return handler
			
		# Return default message if path doesn't exist
		self.error_response(response)
		return response