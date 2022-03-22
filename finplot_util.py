"""
finplot_util.py 

This file stores functions used to support finplot
"""


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


if __name__ == '__main__':
	print('do stuff here')