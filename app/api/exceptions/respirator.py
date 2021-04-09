from werkzeug.exceptions import HTTPException


class MalformedURL(HTTPException):
    code = 422
    data = {"message": "URL Parameter is malformed"}


class RespiratorNotFound(HTTPException):
    code = 404
    data = {"message": "Respirator not found"}


class CannotOpenWebsite(HTTPException):
    code = 599
    data = {"message": "Cannot Open Website"}


class ErrorParsingWebsite(HTTPException):
    code = 599
    data = {"message": "Error Parsing Website"}


class CannotCheckACWebsite(HTTPException):
    code = 599
    data = {"message": "Cannot Check AC Website"}


class ErrorParsingACWebsite(HTTPException):
    code = 599
    data = {"message": "Error Parsing AC Website"}