import jwt
from jwt.exceptions import InvalidSignatureError
import app.config as config

def encode_token(**kwargs):
	return jwt.encode(kwargs, config.SECRET, algorithm=config.JWT_ALGO)

def decode_token(token):
	if token is None:
		return None
	try:
		return jwt.decode(token, config.SECRET, algorithms=[config.JWT_ALGO])
	except: #InvalidSignatureError:
		return None
