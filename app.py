from meteor import Request, Response

def mets(function):
    def application(environ, start_response):
        request = Request(environ)
        response = function(request)
        start_response(response.status, response.headers.items())
        return iter(response)
    return application

@mets
def app(request):
    name = request.args.get('name', 'HanslettThedev')
    return Response([f"<h1>Hello world this is {name}</h1>"])