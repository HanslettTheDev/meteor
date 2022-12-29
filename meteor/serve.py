import http.client as cp
from wsgiref.headers import Headers
import urllib.parse

class Request:
	def __init__(self, environ):
		self.environ = environ
	
	@property
	def args(self):
		get_args = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
		return {k:v[0] for k,v in get_args.items()}

	@property
	def path(self):
		return self.environ["RAW_URI"]

class Response:
	def __init__(self, response=None, status_code=200, charset="utf-8", content_type="text/html"):
		self.headers = Headers()
		self.response = [] if response is None else response
		self.charset = charset
		self.status_code = status_code
		self.headers.add_header('content_type', f"{content_type}; charset={charset}")	

	@property
	def status(self):
		status_to_string = cp.responses.get(self.status_code, "UNKNOWN")
		return f'{self.status_code} {status_to_string}'
	
	def __iter__(self):
		# loop over the list and check for byte objects and return them
		# if they are not encoded, encode and send them
		for response in self.response:
			if isinstance(response, bytes):
				yield response
			else:
				yield response.encode(self.charset)
