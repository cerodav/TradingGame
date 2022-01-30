import json
from enum import Enum
from datetime import datetime
from tornado.web import RequestHandler
from monie.service.type.types import ResponseType

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

class BaseHandler(RequestHandler):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET", "DELETE", "POST", "OPTIONS"]

    def get(self):
        pass

    def setPathInfo(self):
        path = self.request.path
        splits = path.split('/')
        self.pathInfo = {x-2:splits[x] for x in range(2, len(splits))}

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Expose-Headers", "Content-Disposition")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE')
        if 'Content-Type' not in self._headers:
            self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')


    def send_response(self, data, state=ResponseType.SUCCESS):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(state.value)
        response = {
            'status': state.name,
            'data': data
        }
        jsonData = json.dumps(response, cls=CustomJsonEncoder).replace("</", "<\\/")
        self.write(jsonData)

    def send_response_csv(self, data, state=ResponseType.SUCCESS):
        """Construct and send a CSV response with appropriate status code."""
        fileName, filePath = data['name'], data['path']
        self.set_status(state.value)
        self.set_header('Content-type', 'text/csv')
        self.set_header('Content-Disposition', 'attachment; filename="{}"'.format(fileName))
        self.write(open(filePath, 'rb').read())

    def options(self, *args):
        self.set_status(204)
        self.finish()

    def prepare(self):
        self.setPathInfo()

    def throwError(self, eType=ResponseType.NOT_FOUND):
        self.send_response({}, state=eType)