from app import api
from app.resources.account import AccountResource
from app.resources.login import LoginResource
from app.resources.todos import ListsResource, ListsByIdResource, TodosResource, TodosByIdResource


api.add_resource(AccountResource, '/api/account')
api.add_resource(LoginResource, '/api/login')
api.add_resource(ListsResource, '/api/lists')
api.add_resource(ListsByIdResource, '/api/lists/<int:id_list>')
api.add_resource(TodosResource, '/api/lists/todos/<int:id_list>')
api.add_resource(TodosByIdResource, '/api/lists/todos/<int:id_list>/<int:id_todo>')
