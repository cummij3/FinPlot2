"""
account.py

Account class that allows you to input data to an account
"""

import math
import datetime

class Account():
	def __init__(self, name):
		self.name = name
		self.data = dict()
		self.fields = ['Ending Balance', 'Withdrawals and Contributions']
		self.tags = list()

	def __repr__(self):
		return self.name

	def get_name(self):
		""" get name """
		return self.name

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

	def remove_field(self, field_name):
		""" remove field """
		self.fields.remove(field_name)

	def get_fields(self):
		""" return fields """
		return self.fields

	def add_tag(self, tag):
		""" add a tag to the account """
		self.tags.append(tag)

	def get_tags(self):
		""" get account tags """
		return self.tags

	def get_closest_past_date(self, input_date):
		""" return the closest date that is in the past """
		dates = self.data.keys()
		smallest_diff = datetime.timedelta(days=10000000)
		#input_date = datetime.datetime.strptime(input_date, '%Y%m%d')
		closest_date = None
		for date in dates:
			date = datetime.datetime.strptime(date, '%Y%m%d')
			if input_date > date:
				if input_date - date < smallest_diff:
					closest_date = date
					smallest_diff = input_date - date

		return closest_date

if __name__ == '__main__':
	test_acc = Account('cool bank')
	test_acc.add_data('20220202', {'Ending Balance': '10', 'Withdrawals and Contributions':'16'})
	test_acc.add_data('20220302', {'Ending Balance': '26', 'Withdrawals and Contributions':'6'})
	test_acc.add_data('20230302', {'Ending Balance': '26', 'Withdrawals and Contributions':'6'})
	print('closest date:', test_acc.get_closest_past_date('20240203'))
