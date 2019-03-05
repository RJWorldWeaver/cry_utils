#!/usr/bin/python
"""
Gets all Icon names
Chris Sprance
Entrada interactive
"""

# glob looks through files in a smart way
import fnmatch
import os


class MisIcons(object):
	"""
	Grabs entities from a folder
	"""

	def __init__(self):
		super(MisIcons, self).__init__()
		self.folder = os.path.abspath(
			os.path.join(os.path.dirname(__file__), '..', '..', '..', "GameSDK", "Libs", "UI", "Inventory", "item_images"))
		self.file_type = '*_48.png'
		self.names = list()  # a list of Icon Names from png files
		self.files = list()  # a list of a png file paths

	def get_all_icon_paths(self):
		"""gets all the xmls files from a self.folder recursively"""
		for root, dirnames, filenames in os.walk(self.folder):
			for filename in fnmatch.filter(filenames, self.file_type):
				self.files.append(os.path.join(root, filename))
		return self.files

	def get_icon_names(self):
		"""strips off directory info and _48.png"""
		for icon_path in self.files:
			self.names.append(os.path.basename(icon_path).replace('_48.png', ''))
		return self.names

	def get_all_names(self):
		"""main process to run after instantiating class"""
		# find all the icon files
		self.get_all_icon_paths()
		# get the names from the icon files
		self.get_icon_names()
		return self.names
