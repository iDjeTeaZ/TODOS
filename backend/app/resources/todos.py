from datetime import datetime
from flask_restful import Resource, reqparse, abort
from app.services.bdd import ListWrapper
from app.services.todos import Todos, Todo
from app.services.status import STATUS, endpoint
from app.services.swagger import Swagger


class ListsResource(Resource):
	@endpoint()
	@Swagger.doc(
	Swagger("Retourner toutes les TODO list de l'utilisateur", ['TODO API'])\
	.response(STATUS.SUCCESS, "JSON représentant toutes les TODO list de l'utilisateur")\
	.response(STATUS.NOT_LOGIN))
	def get(self, user=None):
		return STATUS.SUCCESS, Todos.find_all(owner=user['user'])

	@endpoint()
	@Swagger.doc(
	Swagger('Créer une nouvelle TODO list', ['TODO API'])\
	.body('Nom de la TODO list')\
	.in_body('name', 'string', True)\
	.response(STATUS.SUCCESS, "L'ID de la TODO list créée")\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.NOT_LOGIN))
	def put(self, user=None):
		body_parser = reqparse.RequestParser()
		body_parser.add_argument('name', type=str, required=True, help='Nom de la TODO list manquant')
		args = body_parser.parse_args(strict=True)
		name = args['name']

		id_list = Todos.new_index('id_list')
		Todos.create(id_list, name, user['user'])
		return STATUS.SUCCESS, { 'id_list':id_list }


class ListsByIdResource(Resource):
	@endpoint()
	@Swagger.doc(Swagger('Retourner une TODO list par son ID', ['TODO API'])\
	.in_path('id_list', 'string', True, "L'ID de la TODO list")\
	.response(STATUS.SUCCESS, 'JSON représentant la TODO list')\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def get(self, id_list, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			return STATUS.SUCCESS, todo_list
		return STATUS.BAD_LIST_ID
	
	@endpoint()
	@Swagger.doc(Swagger("Changer le nom d'une TODO list", ['TODO API'])\
	.body('Le nouveau nom')\
	.in_body('name', 'string', True)\
	.in_path('id_list', 'string', True, "L'ID de la TODO list")\
	.response(STATUS.SUCCESS)\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def patch(self, id_list, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			body_parser = reqparse.RequestParser()
			body_parser.add_argument('name', type=str, required=True, help='Nom de la TODO list manquant')
			args = body_parser.parse_args(strict=True)
			name = args['name']

			todo_list['name'] = name
			Todos.save()
			return STATUS.SUCCESS
		return STATUS.BAD_LIST_ID
	
	@endpoint()
	@Swagger.doc(Swagger('Supprimer une TODO list', ['TODO API'])\
	.in_path('id_list', 'string', True, "L'ID de la TODO list")\
	.response(STATUS.SUCCESS)\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def delete(sef, id_list, user=None):
		if Todos.delete_one(id_list=id_list, owner=user['user']):
			return STATUS.SUCCESS
		return STATUS.BAD_LIST_ID


class TodosResource(Resource):
	@endpoint()
	@Swagger.doc(Swagger("Retourner les TODOs d'une liste par son ID", ['TODO API'])\
	.in_path('id_list', 'string', True, "L'ID de la TODO list")\
	.response(STATUS.SUCCESS, 'Liste JSON représentant les TODOs')\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def get(self, id_list, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			return STATUS.SUCCESS, todo_list['todos']
		return STATUS.BAD_LIST_ID

	@endpoint()
	@Swagger.doc(Swagger('Créer un nouveau TODO dans une TODO list', ['TODO API'])\
	.body("Le nom et le contenu d'un TODO")\
	.in_body('name', 'string', True)\
	.in_body('task', 'string', True)\
	.in_path('id_list', 'string', True, "L'ID de la TODO list")\
	.response(STATUS.SUCCESS, "L'ID du TODO créé")\
	.response(STATUS.MISSING_PARAM)\
	.response(STATUS.BAD_LIST_ID)\
	.response(STATUS.NOT_LOGIN))
	def put(self, id_list, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			todo_list = ListWrapper(todo_list['todos'], Todo)
			id_todo = todo_list.new_index('id_todo')

			body_parser = reqparse.RequestParser()
			body_parser.add_argument('name', type=str, required=True, help='Nom du TODO manquant')
			body_parser.add_argument('task', type=str, required=True, help='Tâche du TODO manquante')
			args = body_parser.parse_args(strict=True)
			name = args['name']
			task = args['task']

			todo_list.create(id_todo, name, task)
			Todos.save()
			return STATUS.SUCCESS, { 'id_todo':id_todo }
		return STATUS.BAD_LIST_ID


def on_todo(f):
	def wrapper(self, id_list, id_todo, user=None):
		todo_list = Todos.find_one(id_list=id_list, owner=user['user'])
		if todo_list:
			todo_list = ListWrapper(todo_list['todos'], Todo)
			result = f(todo_list, id_todo)
			if result is not None:
				return result
			return STATUS.BAD_TODO_ID
		return STATUS.BAD_LIST_ID
	return wrapper

class TodosByIdResource(Resource):
	@endpoint()
	@Swagger.doc(Swagger("Retourner un TODO par son ID et l'ID de la liste", ['TODO API'])\
	.in_path('id_list', 'string', True, "L'ID de la TODO list")\
	.in_path('id_todo', 'string', True, "L'ID du TODO")\
	.response(STATUS.SUCCESS, 'JSON représentant du TODO')\
	.response(STATUS.MISSING_PARAM)\
	.response(404, 'ID de liste ou ID de TODO invalide')\
	.response(STATUS.NOT_LOGIN))
	@on_todo
	def get(todo_list, id_todo):
		todo = todo_list.find_one(id_todo=id_todo)
		if todo:
			return STATUS.SUCCESS, todo

	@endpoint()
	@Swagger.doc(Swagger('Changer un TODO', ['TODO API'])\
	.body('Les nouveaux nom et contenu du TODO')\
	.in_body('name', 'string', False)\
	.in_body('task', 'string', False)\
	.in_path('id_list', 'string', True, "L'ID de la TODO list")\
	.in_path('id_todo', 'string', True, "L'ID du TODO")\
	.response(STATUS.SUCCESS)\
	.response(STATUS.MISSING_PARAM)\
	.response(404, 'ID de liste ou ID de TODO invalide')\
	.response(STATUS.NOT_LOGIN))
	@on_todo
	def patch(todo_list, id_todo):
		todo = todo_list.find_one(id_todo=id_todo)
		if todo:
			body_parser = reqparse.RequestParser()
			body_parser.add_argument('name', type=str, required=False, help='Nom du TODO manquant')
			body_parser.add_argument('task', type=str, required=False, help='Tâche du TODO manquante')
			args = body_parser.parse_args(strict=False)
			name = args['name']
			task = args['task']

			if name is not None: todo['name'] = name
			if task is not None: todo['task'] = task
			todo['date'] = str(datetime.now())
			Todos.save()
			return STATUS.SUCCESS

	@endpoint()
	@Swagger.doc(Swagger('Supprimer un TODO', ['TODO API'])\
	.in_path('id_list', 'string', True, "L'ID de la TODO list")\
	.in_path('id_todo', 'string', True, "L'ID du TODO")\
	.response(STATUS.SUCCESS)\
	.response(404, 'ID de liste ou ID de TODO invalide')\
	.response(STATUS.NOT_LOGIN))
	@on_todo
	def delete(todo_list, id_todo):
		if todo_list.delete_one(id_todo=id_todo):
			Todos.save()
			return STATUS.SUCCESS
