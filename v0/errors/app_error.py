class App_Error(BaseException):
    status = None
    message = ""

    def __init__(self, message, status):
        self.message = message
        self.status = status

    def toHttp(self):
        return {"error": {"message": self.message}}
