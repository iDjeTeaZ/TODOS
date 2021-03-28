from datetime import datetime
from app.services.bdd import BDD
from app import config


class TodoList:
	def __init__(self, id_list, name, owner, todos=[]):
		self.id_list = id_list
		self.name = name
		self.owner = owner
		self.todos = todos
	
	def set(self, name):
		self.name = name
		Todos.save()

class Todo:
	def __init__(self, id_todo, name, task):
		self.id_todo = id_todo
		self.name = name
		self.task = task
		self.date = str(datetime.now())
	
	def set(self, name, task):
		self.name = name
		self.task = task
		self.date = str(datetime.now())
		Todos.save()


if config.MOCK_BDD:
	Todos = BDD(None, TodoList)
else:
	Todos = BDD('app/storage/todos.json', TodoList, 4)
Todos.add_mapping('id_list')
Todos.add_mapping('owner')
