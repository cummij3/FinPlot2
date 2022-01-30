"""
account.py

Account class that allows you to input data to an account
"""

class Account():
	def __init__(self, name):
		self.name = name
		self.data = {}
		self.fields = ['date', 'balance', 'contribuition']

	def add_data(self, date, val_dict):
		"""
		add data

		date format is yyyymmdd
		val_dict format is {key1:value1, ...}
		"""

		self.data['date'] = val_dict

	def get_data(self):
		""" return data """
		return self.data

	def add_field(self, feild_name):
		""" add feild """
		self.fields.append(str(feild_name))

	def get_fields(self):
		""" return fields """
		return self.fields