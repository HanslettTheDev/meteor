from meteor import Meteor
from meteor import Response
from meteor import Request

app = Meteor()

@app.route("/")
@app.route("/hello")
def hello(request: Request):
	return Response(['''
	<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My webpage</title>
</head>
<body>
    <h1>Hello world</h1>
    <h2>Hello box</h2>
    <h3>sdsds</h3>
    <h4>hdss</h4>
    <h5>saksk</h5>
    <h6>akskssa</h6>
</body>
</html>
	'''])

@app.route("/group")
def group(request: Request):
	name = request.args.get('name', 'HanslettThedev')
	return Response([f"<h1>Hello world this is {name}</h1>"])

@app.route("/group/{id}/{name}")
def new(request: Request, id, name):
    # print(request.path)
    return Response([f'<html>Here is the id {id} and {name}</html>'])