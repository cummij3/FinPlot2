"""
finplot.py

finplot will plot data from the account class
"""

import tkinter as tk
from tkinter import filedialog
import os
import account



def finplot(file=None):
	"""
	finplot

	file is the data file used to import data
	"""
	if file:
		print(file)

	os.system('clear')	# use 'cls' for windows

	landing_page()


def landing_page():
	""" first page seen """
	print('-'*50)
	print('What would you like to do?\n')
	choice_dict = {
				'Import Data': exit_program,
				'Plot Data': exit_program,
				'Save Data': exit_program,
				'Exit': exit_program
				}

	show_user_interface(choice_dict)



def show_user_interface(choice_dict):
	""" build the user interface """
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
		show_user_interface(choice_dict)


def exit_program():
	""" end the program """
	print('Exiting Program...')


if __name__ == '__main__':
	#file_path = filedialog.askopenfilename()
	#finplot(file_path)
	finplot()
