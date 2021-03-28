from flask_restful import Resource, reqparse, abort
from app.services.users import Users
from app.services.status import STATUS, endpoint
from app.services.swagger import Swagger


class AccountResource(Resource):
	@endpoint(restricted=False)
	@Swagger.doc(Swagger('Créer un nouvel utilisateur', ['User API'], jwt=False)\
	.body("L'identifiant et le mot de passe de l'utilisateur")\
	.in_body('user', 'string', True)\
	.in_body('pwd', 'string', True)\
	.response(STATUS.SUCCESS)\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.USERNAME_USED))
	def post(self):
		body_parser = reqparse.RequestParser()
		body_parser.add_argument('user', type=str, required=True, help='Identifiant manquant')
		body_parser.add_argument('pwd',  type=str, required=True, help='Mot de passe manquant')
		args = body_parser.parse_args(strict=True)
		user = args['user']
		pwd  = args['pwd']
		return create(user, pwd)

def create(user, pwd):
	u = Users.find_one(user=user)
	if u:
		return STATUS.USERNAME_USED
	Users.create(user, pwd)
	return STATUS.SUCCESS
