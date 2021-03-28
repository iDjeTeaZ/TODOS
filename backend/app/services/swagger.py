class Swagger:
	def __init__(self, description, tags=[], jwt=True):
		self.description = description
		self.tags = tags
		self.body_description = None
		self.parameters_path = []
		self.parameters_head = []
		self.parameters_body = []
		self.responses = []
		if jwt:
			self.in_head('jwt', 'string', True, 'The authentication token')

	def body(self, description):
		self.body_description = description
		return self
	def in_body(self, name, type, required=False, description=None):
		self.parameters_body.append((name, type, required, description))
		return self
	def in_path(self, name, type, required=False, description=None):
		self.parameters_path.append((name, type, required, description))
		return self
	def in_head(self, name, type, required=False, description=None):
		self.parameters_head.append((name, type, required, description))
		return self
	def response(self, status, description=None):
		if type(status) != int:
			self.responses.append((status.exit, description or status.message))
		else:
			self.responses.append((status, description))
		return self

	def __str__(self):
		doc = f'''
		{self.description}
		---
		tags:'''+''.join(f'''
		  - {tag}''' for tag in self.tags)
		if self.parameters_path or self.parameters_body or self.parameters_head:
			doc += f'''
		parameters:'''
		doc += ''.join(f'''
		  - in: path
		    name: {name}
		    description: {description}
		    required: {str(required).lower()}
		    type: {type}''' for name, type, required, description in self.parameters_path)
		doc += ''.join(f'''
		  - in: header
		    name: {name}
		    description: {description}
		    required: {str(required).lower()}
		    type: {type}''' for name, type, required, description in self.parameters_head)
		if self.parameters_body:
			doc += f'''
		  - in: body
		    name: attributes
		    description: {self.body_description}
		    schema:
		      type: object
		      properties:'''+''.join(f'''
		        {name}:
		          type: {type}
		          description: {description}''' for name, type, _, description in self.parameters_body)
		if any(parameter[2] for parameter in self.parameters_body):
			doc += f'''
		      required:'''+''.join(f'''
		        - {name}''' for name, _, required, _ in self.parameters_body if required)
		if self.responses:
			doc += f'''
		responses:'''+''.join(f'''
		  {code}:
		    description: {description}''' for code, description in self.responses)
		doc = '\n'.join(line for line in doc.split('\n') if ': None' not in line)
		return doc

	def doc(swagger):
		def swaggify(f):
			f.__doc__ = str(swagger)
			return f
		return swaggify
