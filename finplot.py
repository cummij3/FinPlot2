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
		self.back_str = 'Go Back'
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
				try:
					if int(filename[0:8]+filename[9:15]) > int(latest_filename[0:8]+latest_filename[9:15]):
						latest_filename = filename
				except:
					print('Error in __init__: there are some bad files in this directory')

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
					'Plot Data': self.plot_data_ui,
					'Create Account': self.create_account,
					'Edit Account': self.edit_account,
					'Import Data': self.import_data_redirect,
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
							if field not in temp_account.get_fields():
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
				account = self.choose_account_ui()
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
				return
			elif choice == choice_list.index('Remove Field'):
				self.remove_account_field(account)
				self.edit_account(account)
				return
			elif choice == choice_list.index('Delete Account'):
				self.delete_account(account)
				self.landing_page()
				return
			elif choice == choice_list.index('Go Back'):
				self.landing_page()
				return
			else:
				assert True, 'Error in edit_account'
				self.edit_account(account)
				self.landing_page()
				return

		except AssertionError as msg:
			print(msg)
			print('Error in edit_account')
			self.landing_page()

	def add_account_field(self, account):
		""" add account field """
		account.add_field(input('Input Field Name: '))

	def remove_account_field(self, account):
		""" remove account field """
		account.remove_field(input('Input Field Name: '))

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

	def input_account_data(self, account=None):
		""" input data """
		try:
			if not account:
				account = self.choose_account_ui()
			assert account != None, 'No account chosen'
			print('\nData Input:')
			date = input('\nDate: ')
			assert fpu.is_date_valid(date), "Exception Error 420: Bad Date Input"

			print('\nAccount Fields:')
			for field in account.get_fields():
				print(field)
			print()

			input_data = {}
			for field in account.get_fields():
				user_input = input(f'{field}: ')
				assert fpu.is_data_valid(user_input), "Exception Error 69: Bad Input"
				input_data[field] = float(user_input)
			account.add_data(date, input_data)
			print('\n', input_data)

			self.landing_page()
			return

		except AssertionError as msg:
			print(msg)
			self.landing_page()
			return

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

	def choose_account_ui(self):
		""" choose account from accounts """
		try:
			choice_list = []
			for account in self.accounts:
				choice_list.append(account.get_name())
			choice_list.append(self.back_str)

			assert len(choice_list) != 0, 'No accounts exist. Create an account before adding data'

			print('\nChoose Account: ')
			choice = fpu.choice_user_interface(choice_list)

			if choice_list[choice] == self.back_str:
				return self.back_str

			account_name = choice_list[choice]
			print('That account is: ', account_name)

			for val in self.accounts:
				if account_name == val.get_name():
					account = val
					break

			return account
		except AssertionError as msg:
			print(msg)
			print('Error in choose_account_ui')
			return None

	def plot_data_ui(self):
		""" plot data ui """
		print(self.dashes)
		print('Choose from the below plot options:\n')
		choice_dict = {
					'Plot Account Data': self.plot_account_data,
					'Plot Tag Data': self.plot_tag_data,
					'Plot Latest Values': self.plot_latest_values
					}

		fpu.function_user_interface(choice_dict)

	def plot_account_data(self):
		""" plot data from accounts """
		try:
			account = self.choose_account_ui()
			if account == self.back_str:
				self.landing_page()
				return
			data = account.get_data()
			print(data)
			dates = list()
			for date in data.keys():
				dates.append(int(date))
			#dates.sort()
			plot_data = {}
			for date in dates:
				for prop in data[str(date)]:
					if prop not in plot_data:
						plot_data[prop] = [[], []]
					print(datetime.datetime.strptime(str(date), '%Y%m%d'), data[str(date)][prop])
					plot_data[prop][0].append(datetime.datetime.strptime(str(date), '%Y%m%d'))
					plot_data[prop][1].append(float(data[str(date)][prop]))

				#x_vals.append(datetime.datetime.strptime(date, '%Y%m%d'))
				#z_vals.append(float(data[date]['Ending Balance']))
				#print(date, data[date]['Ending Balance'])

			for prop in plot_data:
				plt.plot(plot_data[prop][0], plot_data[prop][1], label=prop)
			plt.legend()
			plt.title(account.get_name())
			plt.xlabel('Date')
			plt.ylabel('$')
			plt.show()

			self.landing_page()
			return

		except BaseException as err:
			print(f"Error in plot_account_data: {err}, {type(err)}")
			self.landing_page()
		except:
			print('Error in plot_account_data')
			self.landing_page()
			return

	def plot_tag_data(self):
		""" plot the sum of account fields that have a tag """
		try:
			# Choose tag
			tags = list()
			for account in self.accounts:
				acc_tags = account.get_tags()
				for acc_tag in acc_tags:
					if acc_tag not in tags:
						tags.append(acc_tag)
			tag = tags[fpu.choice_user_interface(tags, "Choose account tag: ")]

			# Build account list
			account_list = list()
			for account in self.accounts:
				if tag in account.get_tags():
					account_list.append(account)

			# Structure plot data
			plot_data = list()
			for account in account_list:
				x_vals, y_vals = list(), list()
				data = account.get_data()
				for date in data:
					x_vals.append(datetime.datetime.strptime(str(date), '%Y%m%d'))
					y_vals.append(float(data[str(date)]['Ending Balance']))
				plot_data.append({'name':account.get_name(), 'x_vals': x_vals, 'y_vals': y_vals})

			# structure sum data
			x_vals, y_vals = list(), list()
			date_list = list()
			for idx in range(len(plot_data)):
				date_list += plot_data[idx]['x_vals']
			min_date = min(date_list)
			max_date = max(date_list)

			date = min_date
			while date < max_date:
				val_sum = 0
				for account in account_list:
					closest_date = account.get_closest_past_date(date)
					if closest_date:
						val_sum += float(account.get_data()[datetime.datetime.strftime(closest_date, "%Y%m%d")]['Ending Balance'])
				x_vals.append(date)
				y_vals.append(val_sum)
				date += datetime.timedelta(weeks=4)
			plot_data.append({'name':'total', 'x_vals': x_vals, 'y_vals': y_vals})
			# Plot data
			for idx in range(len(plot_data)):
				plt.plot(plot_data[idx]['x_vals'], plot_data[idx]['y_vals'], label=plot_data[idx]['name'])

			plt.legend()
			plt.title(tag)
			plt.xlabel('Date')
			plt.ylabel('$')
			plt.show()

			self.landing_page()

		except BaseException as err:
			print(f"Error in plot_tag_data: {err}, {type(err)}")
			self.landing_page()
		except:
			print('Error in plot_tag_data')
			self.landing_page()
			return

	def plot_latest_values(self):
		""" plot the latest values in a pie chart """
		print('plot_latest_values')

		# build dict of form {tag:[accounts with tag]}
		tag_dict = {}
		for account in self.accounts:
			tags = account.get_tags()
			for tag in tags:
				if tag not in tag_dict:
					tag_dict[tag] = [account]
				else:
					tag_dict[tag].append(account)

		# build dict of form {tag:sum of account value with tag}
		sum_dict = {}
		figs, fig_count = [], 1
		for tag in tag_dict:
			plot_data = {'vals': [], 'labels': [], 'title': ''}
			tag_sum = 0
			for account in tag_dict[tag]:
				val = float(account.get_latest_data()['Ending Balance'])
				if val != 0:
					tag_sum += val
					plot_data['vals'].append(val)
					plot_data['labels'].append(account.get_name())
			sum_dict[tag] = tag_sum
			print(f"{tag} Total: ", tag_sum)
			plot_data['title'] = tag + ' - total = ' + "${:,.0f}".format(tag_sum)

			figs.append(plt.figure(fig_count))
			print(len(plot_data['vals']), len(plot_data['labels']))
			plt.pie(plot_data['vals'], labels=plot_data['labels'])
			plt.title(plot_data['title'])
			fig_count += 1
		plt.show()


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
