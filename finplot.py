"""
finplot.py

finplot will plot data from the account class
"""

import tkinter as tk
from tkinter import filedialog
import os
import account
import json
import matplotlib.pyplot as plt



class FinPlot():
	def __init__(self, file=None):

		os.system('clear')	# use 'cls' for windows
		self.accounts = []

		if file:
			self.import_data(file)

		self.landing_page()


	def landing_page(self):
		""" first page seen """
		print('-'*50)
		print('What would you like to do?\n')
		choice_dict = {
					'Import Data': self.import_data,
					'Input Data': self.exit_program,
					'Plot Data': self.plot_data,
					'Save Data': self.exit_program,
					'Exit': self.exit_program
					}

		self.function_user_interface(choice_dict)


	def function_user_interface(self, choice_dict):
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
			self.function_user_interface(choice_dict)

	def choice_user_interface(self, choice_list):
		""" build the user interface """
		valid_choices = range(len(choice_list))
		for idx, val in enumerate(choice_list):
			print(f'[{idx}] {val}')
		choice = int(input('\nUser input: '))
		if choice in valid_choices:
			print('\nyou chose: ', choice_list[choice])
		else:
			print("\nInvalid input. Try again")
			self.choice_user_interface(choice_list)

		return choice

	def import_data(self, file_path=None):
		""" import data from json """
		if file_path is None:
			file_path = filedialog.askopenfilename()
		with open(file_path) as file:
			data = json.load(file)

		for acc_name in data:
			temp_account = account.Account(acc_name)
			self.accounts.append(temp_account)
			for key in data[acc_name]:
				if key == 'tags':
					for tag in data[acc_name][key]:
						temp_account.add_tag(tag)
				if key == 'properties':
					for field in data[acc_name][key]:
						temp_account.add_field(field)
				if key == 'data':
					for date in data[acc_name][key]:
						temp_account.add_data(date, data[acc_name][key][date])

	def plot_data(self):
		""" plot data from accounts """
		choice_list = []
		for account in self.accounts:
			choice_list.append(account.get_name())

		account_name = self.choice_user_interface(choice_list)

		for val in self.accounts:
			if account_name == val.get_name():
				account = val
				break

		data = account.get_data()
		print(data)
		x_vals, z_vals= [], []
		for date in data:
			x_vals.append(date)
			z_vals.append(data[date]['Ending Balance'])
			print(date, data[date]['Ending Balance'])


		# red dashes, blue squares and green triangles
		plt.plot(x_vals, z_vals)
		plt.show()


	def exit_program(self):
		""" end the program """
		print('Exiting Program...')


if __name__ == '__main__':
	#file_path = filedialog.askopenfilename()
	#finplot(file_path)
	FinPlot('C:/Users/Jed/Downloads/json_data - Copy.json')
