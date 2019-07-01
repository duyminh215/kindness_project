from flask import jsonify


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, error_message, payload=None):
        Exception.__init__(self)
        self.message = error_message['message']
        self.error_code = error_message['error_code']
        if error_message['status_code'] is not None:
            self.status_code = error_message['status_code']
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['error_code'] = self.error_code
        return rv
