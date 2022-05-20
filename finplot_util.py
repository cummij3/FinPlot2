"""
finplot_util.py 

This file stores functions used to support finplot
"""

import datetime


def function_user_interface(choice_dict):
	"""
	build the user interface

	choice dict: {choice1: function1, ...}
	"""
	choice_list = list()
	[choice_list.append(key) for key in choice_dict]
	valid_choices = range(len(choice_list))
	for idx, val in enumerate(choice_list):
		print(f'[{idx}] {val}')
	choice = int(input('\nUser input: '))
	if choice in valid_choices:
		print('\nyou chose: ', choice_list[choice])
		choice_dict[choice_list[choice]]()
	else:
		print("\nInvalid input. Try again")
		function_user_interface(choice_dict)

def choice_user_interface(choice_list, user_prompt=None):
	"""
	build the user interface
	choice_list: list of choices
	user_prompt: message to display to the user
	returns the index chosen
	"""
	try:
		print()
		if user_prompt:
			print(user_prompt)
		else:
			print('Choose option from the below list: ')

		valid_choices = range(len(choice_list))
		for idx, val in enumerate(choice_list):
			print(f'[{idx}] {val}')
		choice = int(input('\nUser input: '))
		if choice in valid_choices:
			print('\nyou chose: ', choice_list[choice])
		else:
			print("\nInvalid input. Try again")
			choice = choice_user_interface(choice_list)

		return choice

	except:
		print('\nsomething weird happened\n')
		return None

def is_date_valid(date):
	""" check in date input is valid """
	try:
		datetime.datetime.strptime(date, '%Y%m%d')
		return True
	except:
		return False

def is_data_valid(data):
	""" check if data is valid """
	try:
		float(data)
		return True
	except:
		print(f'Error in is_data_valid: {data} cannot be converted to float')
		return False


if __name__ == '__main__':
	print('do stuff here')
