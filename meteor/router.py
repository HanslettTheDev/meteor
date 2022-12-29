class Router:
    def __init__(self, route: str, request_path: str):
        self.route = route
        self.request_path = request_path
        self.vars = list()
        self.url = ""
        self.break_routes()
    
    def break_routes(self):
        # remove any empty items in the list and return the lists
        self.rts = list(filter(None, self.route.split("/")))
        self.reqpath = list(filter(None, self.request_path.split("/")))

    def compare_routes(self):
        '''Compare the routes strings step by step
        checking the routes to see if there is any variable to be passed
        '''
        if len(self.rts) != len(self.reqpath):
            return 404

        url = ""

        for rts, reqp in zip(self.rts, self.reqpath):
            if rts != reqp:
                if rts.startswith("{") and rts.endswith("}"):
                    url += "/" + reqp
                    self.vars.append(reqp)
                    continue
            url += "/" + reqp
        
        return url

    def start(self):
        result = self.compare_routes()
        if result != 404:
            return result

    @property
    def hasVar(self):
        '''Returns a bool if a variable was passed in the function'''
        return True if self.vars else False