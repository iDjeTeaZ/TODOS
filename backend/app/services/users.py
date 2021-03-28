from app.services.bdd import BDD
from app.services.jwt import encode_token
from app import config
import hashlib


class User:
	def __init__(self, user, pwd):
		self.user = user
		self.pwd = User.hash(pwd)

	def get_token(self):
		return encode_token(user=self.user)

	def __str__(self):
		return f'User[{self.user}, {self.pwd}]'
	
	def hash(pwd):
		return hashlib.md5(pwd.encode()).hexdigest()


if config.MOCK_BDD:
	Users = BDD(None, User)
else:
	Users = BDD('app/storage/users.json', User, 4)
