"""
finplot.py

finplot will plot data from the account class
"""

import tkinter as tk
from tkinter import filedialog
import account

def finplot(file):
	""" finplot """
	print(file)


if __name__ == '__main__':
	file_path = filedialog.askopenfilename()
	finplot(file_path)
