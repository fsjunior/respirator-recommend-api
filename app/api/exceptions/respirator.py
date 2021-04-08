from werkzeug.exceptions import HTTPException


class RespiratorNotFound(HTTPException):
    code = 404
    data = {"message": "Respirator not found"}
