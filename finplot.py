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
import time
import datetime



class FinPlotUI():
	def __init__(self, file=None):

		os.system('clear')	# use 'cls' for windows
		self.accounts = []
		self.dashes = '-'*50

		if file:
			self.import_data(file)
		else:
			file = self.load_file_ui()
			self.landing_page()


	def landing_page(self):
		""" first page seen """
		print(self.dashes)
		print('What would you like to do?\n')
		choice_dict = {
					'Import Data': self.import_data,
					'Input Data': self.exit_program,
					'Plot Data': self.plot_data,
					'Save Data': self.exit_program,
					'Exit': self.exit_program
					}

		self.function_user_interface(choice_dict)

	def load_file_ui(self):
		""" load file or start with blank file """
		print(self.dashes)
		print('Woulld you like to import data from a file?\n')
		choice_list = ['Yes', 'No']
		for idx, choice in enumerate(choice_list):
			print(f'[{idx}] {choice}')
		choice = int(input('\nUser input: '))
		if choice == 0:
			print('You chose "Yes"')
			file = filedialog.askopenfilename()
		elif choice == 1:
			print('You chose "No"')
			file = None
		else:
			print('invalid choice')
			time.sleep(2)
			self.load_file_ui()
		time.sleep(2)
		os.system('clear')

		return file

	def function_user_interface(self, choice_dict):
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

		print('Data imported from: ', file_path)
		time.sleep(2)
		self.landing_page()

	def plot_data(self):
		""" plot data from accounts """
		choice_list = []
		for account in self.accounts:
			choice_list.append(account.get_name())

		choice = self.choice_user_interface(choice_list)
		account_name = choice_list[choice]
		print('That account is: ', account_name)

		for val in self.accounts:
			if account_name == val.get_name():
				account = val
				break

		print('That account is: ', account)

		data = account.get_data()
		print(data)
		x_vals, z_vals= [], []
		plot_data = {}
		for date in data:
			for prop in data[date]:
				if prop not in plot_data:
					plot_data[prop] = [[], []]
				print(datetime.datetime.strptime(date, '%Y%m%d'), data[date][prop])
				plot_data[prop][0].append(datetime.datetime.strptime(date, '%Y%m%d'))
				plot_data[prop][1].append(float(data[date][prop]))

			#x_vals.append(datetime.datetime.strptime(date, '%Y%m%d'))
			#z_vals.append(float(data[date]['Ending Balance']))
			#print(date, data[date]['Ending Balance'])


		# red dashes, blue squares and green triangles
		for prop in plot_data:
			plt.plot(plot_data[prop][0], plot_data[prop][1], label=prop)
		plt.legend()
		plt.title(account_name)
		plt.xlabel('Date')
		plt.ylabel('$')
		plt.show()

		self.landing_page()


	def exit_program(self):
		""" end the program """
		print('Exiting Program...')


if __name__ == '__main__':
	#file_path = filedialog.askopenfilename()
	#finplotUI(file_path)
	#FinPlotUI('C:/Users/Jed/Downloads/json_data - Copy.json')
	FinPlotUI('C:/Users/Jed/Downloads/json_data.json')
	#FinPlotUI()
