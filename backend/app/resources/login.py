from flask_restful import Resource, reqparse, abort
from app.services.users import Users, User
from app.services.status import STATUS, endpoint
from app.services.debug import DEBUG
from app.services.swagger import Swagger


class LoginResource(Resource):
	@endpoint(restricted=False)
	@Swagger.doc(Swagger("Se connecter en tant qu'utilisateur", ['User API'], jwt=False)\
	.body("L'identifiant et le mot de passe de l'utilisateur")\
	.in_body('user', 'string', True)\
	.in_body('pwd', 'string', True)\
	.response(STATUS.SUCCESS, "Le token de l'utilisateur")\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.BAD_LOGIN))
	def post(self):
		body_parser = reqparse.RequestParser()
		body_parser.add_argument('user', type=str, required=True, help='Identifiant manquant')
		body_parser.add_argument('pwd',  type=str, required=True, help='Mot de passe manquant')
		args = body_parser.parse_args(strict=True)
		user = args['user']
		pwd  = args['pwd']
		return login(user, pwd)


def login(user, pwd):
	u = Users.find_one(user=user, pwd=User.hash(pwd))
	if u:
		u = Users.decode(u)
		return STATUS.SUCCESS, { 'token':u.get_token() }
	else:
		return STATUS.BAD_LOGIN
