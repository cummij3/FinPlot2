"""
account.py

Account class that allows you to input data to an account
"""

class Account():
	def __init__(self, name):
		self.name = name
		self.data = dict()
		self.fields = ['ending balance', 'contribution']
		self.tags = list()

	def add_data(self, date, val_dict):
		"""
		add data

		val_dict = {field1: val1, ...}
		"""
		self.data[date] = val_dict

	def get_data(self):
		""" return data """
		return self.data

	def add_field(self, feild_name):
		""" add feild """
		self.fields.append(str(feild_name))

	def get_fields(self):
		""" return fields """
		return self.fields

	def add_tag(self, tag):
		""" add a tag to the account """
		self.tags.append(tag)

	def get_tags(self):
		""" get account tags """
		return self.tags
