import json


def constructor(self, properties):
	for key, value in properties.items():
		self.__setattr__(key, value)

class Base:
	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			self.__setattr__(key, value)

class BDD:
	def __init__(self, path=None, model=Base, indent=None):
		self.path = path
		self.model = model
		self.indent = indent
		self.maps = {}
		self.frozen = False
		self.dirty = False
		model_def = dict(model.__dict__)
		model_def['__init__'] = constructor
		self.cast_model = type(model.__name__, model.__bases__, model_def)
		if path is None:
			self.save = lambda:None
			self.local = []
		else:
			self.load()
	
	def load(self):
		with open(self.path, 'r') as stream:
			self.local = json.load(stream)
	def save(self):
		if self.frozen:
			self.dirty = True
			return
		with open(self.path, 'w') as stream:
			json.dump(self.local, stream, indent=self.indent)
	def freeze(self):
		self.frozen = True
	def unfreeze(self):
		self.frozen = False
		if self.dirty:
			self.dirty = False
			self.save()

	def add_mapping(self, key):
		if key in self.maps:
			return
		mapping = {}
		for obj in self.local:
			if obj[key] in mapping:
				mapping[obj[key]].append(obj)
			else:
				mapping[obj[key]] = [obj]
		self.maps[key] = mapping
	def add_to_maps(self, obj):
		for key, mapping in self.maps.items():
			if obj[key] in mapping:
				mapping[obj[key]].append(obj)
			else:
				mapping[obj[key]] = [obj]
	def delete_from_maps(self, obj):
		for key, mapping in self.maps.items():
			mapping[obj[key]].remove(obj)
	
	def encode(self, obj):
		return obj.__dict__
	def decode(self, obj):
		return self.cast_model(obj)
	
	def new_index(self, key):
		return max(self.local, key=lambda obj:obj[key])[key]+1 if self.local else 0

	def create(self, *args, **kwargs):
		obj = self.encode(self.model(*args, **kwargs))
		self.local.append(obj)
		self.save()
		self.add_to_maps(obj)
	def add(self, obj):
		obj = self.encode(obj)
		self.local.append(obj)
		self.save()
		self.add_to_maps(obj)

	def similar(self, obj, **kwargs):
		return all(obj[key] == value for key, value in kwargs.items())
	def best_cut(self, **kwargs):
		cuts = [(key, self.maps[key].get(value, [])) for key, value in kwargs.items() if key in self.maps]
		if cuts:
			return min(cuts, key=lambda cut:len(cut[1]))
		return None, self.local

	def delete_one(self, **kwargs):
		for i, obj in enumerate(self.local):
			if self.similar(obj, **kwargs):
				self.delete_from_maps(self.local[i])
				del self.local[i]
				self.save()
				return True
		return False
	def delete_all(self, **kwargs):
		for i in range(len(self.local)-1, -1, -1):
			if self.similar(self.local[i], **kwargs):
				self.delete_from_maps(self.local[i])
				del self.local[i]
		self.save()

	def find_one(self, **kwargs):
		key, cut = self.best_cut(**kwargs)
		if key is not None:
			del kwargs[key]
		return next(filter(lambda obj:self.similar(obj, **kwargs), cut), None)
	def find_all(self, **kwargs):
		key, cut = self.best_cut(**kwargs)
		if key is not None:
			kwargs[key]
		if kwargs:
			return list(filter(lambda obj:self.similar(obj, **kwargs), cut))
		else:
			return list(cut)


class ListWrapper:
	def __init__(self, local=[], model=Base):
		self.local = local
		self.model = model
		model_def = dict(model.__dict__)
		model_def['__init__'] = constructor
		self.cast_model = type(model.__name__, model.__bases__, model_def)
	
	def encode(self, obj):
		return obj.__dict__
	def decode(self, obj):
		return self.cast_model(obj)

	def new_index(self, key):
		return max(self.local, key=lambda obj:obj[key])[key]+1 if self.local else 0

	def create(self, *args, **kwargs):
		obj = self.encode(self.model(*args, **kwargs))
		self.local.append(obj)
	def add(self, obj):
		obj = self.encode(obj)
		self.local.append(obj)

	def similar(self, obj, **kwargs):
		return all(obj[key] == value for key, value in kwargs.items())

	def delete_one(self, **kwargs):
		for i, obj in enumerate(self.local):
			if self.similar(obj, **kwargs):
				del self.local[i]
				return True
		return False
	def delete_all(self, **kwargs):
		for i in range(len(self.local)-1, -1, -1):
			if self.similar(self.local[i], **kwargs):
				del self.local[i]

	def find_one(self, **kwargs):
		return next(filter(lambda obj:self.similar(obj, **kwargs), self.local), None)
	def find_all(self, **kwargs):
		return list(filter(lambda obj:self.similar(obj, **kwargs), self.local))
