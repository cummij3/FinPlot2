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
import finplot_util as fpu



class FinPlotUI():
	def __init__(self, file=None):

		os.system('clear')	# use 'cls' for windows
		self.accounts = []
		self.dashes = '-'*50
		self.save_path = os.path.join(os.path.expanduser("~"), 'finplot_data')
		os.chdir(self.save_path)
		if not os.path.exists(self.save_path):
			os.makedirs(os.path.abspath(self.save_path))

		if file:
			self.import_data(file)
		else:
			files = os.listdir()
			latest_filename = '00000000'
			for filename in files:
				if int(filename[0:8]) > int(latest_filename[0:8]):
					latest_filename = filename

		if latest_filename != '00000000':
			self.import_data(latest_filename)
		else:
			filename = self.load_file_ui()
			if filename:
				self.import_data(filename)

		self.landing_page()

	def landing_page(self):
		""" first page seen """
		print(self.dashes)
		print('What would you like to do?\n')
		choice_dict = {
					'Input Data': self.input_account_data,
					'Import Data': self.import_data_redirect,
					'Create Account': self.create_account,
					'Edit Account': self.edit_account,
					'Plot Data': self.plot_account_data,
					'Save Data': self.save_data,
					'Exit': self.exit_program
					}

		fpu.function_user_interface(choice_dict)

	def import_data_redirect(self, file_path=None):
		""" The function runs import data then redirects to the landing page """
		self.import_data(file_path)
		self.landing_page()

	def import_data(self, file_path=None):
		""" import data from json """
		try:
			if file_path is None:
				file_path = filedialog.askopenfilename()
			with open(file_path) as file:
				data = json.load(file)

			self.accounts = []
			for acc_name in data:
				temp_account = account.Account(acc_name)
				self.accounts.append(temp_account)
				for key in data[acc_name]:
					if key == 'tags':
						for tag in data[acc_name][key]:
							temp_account.add_tag(tag)
					if key == 'fields':
						for field in data[acc_name][key]:
							temp_account.add_field(field)
					if key == 'data':
						for date in data[acc_name][key]:
							temp_account.add_data(date, data[acc_name][key][date])

			print('Data imported from: ', file_path)
			time.sleep(2)

		except:
			print('Error in import_data')

	def load_file_ui(self):
		""" load file or start with blank file """
		print(self.dashes)
		print('Would you like to import data from a file?\n')
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

	###########################################################################
	def create_account(self):
		""" create account """
		try:
			print('\nCreate Account\n')
			self.accounts.append(account.Account(input('Input account name: ')))
			self.landing_page()
		except:
			print('Error in create_account')
			self.landing_page()

	def edit_account(self, account=None):
		""" edit account """
		try:
			if not account:
				account = self.choose_account()
			assert account != None, 'No account chosen'

			choice_list = [
						'Add Field',
						'Remove Field',
						'Delete Account',
						'Go Back'
						]

			choice = fpu.choice_user_interface(choice_list)

			if choice == choice_list.index('Add Field'):
				self.add_account_field(account)
				self.edit_account(account)
			elif choice == choice_list.index('Remove Field'):
				self.remove_account_field(account)
				self.edit_account(account)
			elif choice == choice_list.index('Delete Account'):
				self.delete_account(account)
				self.edit_account(account)
			elif choice == choice_list.index('Go Back'):
				self.landing_page()
			else:
				assert True, 'Error in edit_account'
				self.edit_account(account)
				self.landing_page()

		except AssertionError as msg:
			print(msg)
			print('Error in edit_account')
			self.landing_page()

	def add_account_field(self, account):
		""" add account field """
		account.add_field(input('Input Field Name: '))

	def remove_account_field(self, account):
		""" remove account field """
		account.remove_field(input('Input Field Nane: '))

	def delete_account(self, account):
		""" delete account """
		try:
			print(f'Are you sure that you want to delete {account.get_name()}?\n')
			choice_list = ['Yes', 'No']
			for idx, choice in enumerate(choice_list):
				print(f'[{idx}] {choice}')
			choice = int(input('\nUser input: '))
			if choice == 0:
				print('You chose "Yes"')
				self.accounts.remove(account)
			elif choice == 1:
				print('You chose "No"')
			else:
				print('invalid choice')
				time.sleep(2)
				self.delete_account(account)
		except:
			print('Error in delete_account')
			self.landing_page()

	####################################
	def input_account_data(self, account=None):
		""" input data """
		try:
			if not account:
				account = self.choose_account()
			assert account != None, 'No account chosen'
			print('\nData Input:')
			date = input('\nDate: ')
			assert self.is_date_valid(date), "Exception Error 420: Bad Date Input"

			print('\nAccount Fields:')
			for field in account.get_fields():
				print(field)
			print()

			input_data = {}
			for field in account.get_fields():
				user_input = input(f'{field}: ')
				assert self.is_data_valid(user_input), "Exception Error 69: Bad Input"
				input_data[field] = float(user_input)
			account.add_data(date, input_data)
			print('\n', input_data)

			self.landing_page()

		except AssertionError as msg:
			print(msg)
			self.landing_page()

	def is_date_valid(self, date):
		""" check in date input is valid """
		ret_val = True
		if len(date) != 8:
			ret_val = False
			print('Invalid Date: ', date)
		elif not date.isnumeric():
			ret_val = False
			print('Invalid Date: ', date)

		return ret_val

	def is_data_valid(self, data):
		""" check if data is valid """
		ret_val = True
		if data == '':
			ret_val = False
			print('Invalid data: ', data, ' - data field is empty')
		elif not data.isnumeric():
			ret_val = False
			print('Invalid data: ', data, ' - data field is not numeric')

		return ret_val

	def save_data(self):
		""" save data to json """
		acc_dict = {}
		for acc in self.accounts:
			acc_dict[acc.get_name()] = acc.__dict__
		json_str = json.dumps(acc_dict, indent=4)
		now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.json'
		with open(os.path.join(self.save_path, now_str), 'w') as outfile:
			outfile.write(json_str)

		self.landing_page()

	def choose_account(self):
		""" choose account from accounts """
		try:
			choice_list = []
			for account in self.accounts:
				choice_list.append(account.get_name())

			assert len(choice_list) != 0, 'No accounts exist. Create an account before adding data'

			print('\nChoose Account: ')
			choice = fpu.choice_user_interface(choice_list)
			account_name = choice_list[choice]
			print('That account is: ', account_name)

			for val in self.accounts:
				if account_name == val.get_name():
					account = val
					break

			return account
		except AssertionError as msg:
			print(msg)
			print('Error in choose_account')
			return None

	def plot_account_data(self):
		""" plot data from accounts """
		try:
			account = self.choose_account()
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
			plt.title(account.get_name())
			plt.xlabel('Date')
			plt.ylabel('$')
			plt.show()

			self.landing_page()
		except:
			print('Error in plot_account_data')
			self.landing_page()


	def exit_program(self):
		""" end the program """
		print('Exiting Program...')


if __name__ == '__main__':
	#file_path = filedialog.askopenfilename()
	#finplotUI(file_path)
	#FinPlotUI('C:/Users/Jed/Downloads/json_data - Copy.json')
	#FinPlotUI('C:/Users/cummi/Downloads/json_data.json')
	FinPlotUI()
