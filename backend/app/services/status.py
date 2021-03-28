from flask import request, make_response
from werkzeug.exceptions import BadRequest
from app import config
from app.services.jwt import decode_token


class Status:
	def __init__(self, code, message, exit):
		self.code = code
		self.message = message
		self.exit = exit

class STATUS:
	SUCCESS			= Status( 0, 'Success', 200)
	NOT_LOGIN		= Status( 1, 'Missing or invalid token', 401)
	MISSING_PARAM	= Status(10, 'Missing or invalid parameter(s)', 400)
	BAD_REQUEST		= Status(11, 'Bad request', 400)
	USERNAME_USED	= Status(20, 'Username already in use', 409)
	BAD_LOGIN		= Status(21, 'Invalid credentials', 401)
	BAD_LIST_ID		= Status(30, 'Invalid TODO list id', 404)
	BAD_TODO_ID		= Status(31, 'Invalid TODO id for this list id', 404)
	def custom_message(status, message=None):
		if message is not None:
			status.message = message
		return status


def formated_response(status, data=None, origin=None):
	content = {
		'status':status.code,
		'message':status.message,
	}

	#Logs.create(status.code, origin)

	if data is not None:
		content['data'] = data
	response = make_response(content, status.exit)

	#if config.CORS is not None:
	#	response.headers['Access-Control-Allow-Origin']=config.CORS
	return response

def endpoint(restricted=True):
	def typed_endpoint(f):
		def wrapper(*args, **kwargs):
			if restricted:
				user = decode_token(request.headers.get('jwt'))
				if user is None:
					return formated_response(STATUS.NOT_LOGIN)
				kwargs['user'] = user
			try:
				result = f(*args, **kwargs)
				if type(result) == Status:
					return formated_response(result, origin=request)
				return formated_response(*result, origin=request)
			except BadRequest as info:
				if 'data' in dir(info):
					default = { 'default': 'Bad request' }
					message = list(info.data.get('message', default).values())[0]
					return formated_response(STATUS.custom_message(STATUS.MISSING_PARAM, message), origin=request)
				return formated_response(STATUS.BAD_REQUEST, origin=request)
		wrapper.__doc__ = f.__doc__
		return wrapper
	return typed_endpoint
