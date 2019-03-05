#!/usr/bin/python
"""
Gets all item names from Scripts/Entities/Items
Chris Sprance
Entrada interactive
"""

# glob looks through files in a smart way
import fnmatch
import os
import re


class MisItems(object):
	"""
	Grabs entities from a folder
	"""

	def __init__(self):
		super(MisItems, self).__init__()
		self.folder = os.path.abspath(
			os.path.join(os.path.dirname(__file__), '..', '..', '..', "GameSDK", "Scripts", "Entities", "Items", "XML"))
		self.file_type = '*.xml'
		self.items = list()
		self.item_names = list()  # a list of ItemNames from xml files
		self.xml_files = list()  # a list of a xml file paths
		self.exclude_list = self.get_excluded_files_list()

	def get_all_xml_paths(self):
		"""gets all the xmls files from a self.folder recursively"""
		for root, dirnames, filenames in os.walk(self.folder):
			for filename in fnmatch.filter(filenames, self.file_type):
				self.xml_files.append(os.path.join(root, filename))
		return self.xml_files

	def get_names_from_xml(self):
		"""gets all the  item names from self.xml_files"""
		for xml in self.xml_files:
			with open(os.path.normpath(xml), 'r') as f:
				x = re.findall(r'"(.*?)"', f.readline())
				if len(x) > 0:
					self.item_names.append(x[0])
		return self.item_names

	def get_all_names(self):
		"""main process to run after instantiating class"""
		# find all the damn cgfs
		self.get_all_xml_paths()
		# get the names from the xml
		self.get_names_from_xml()
		return self.item_names

	@staticmethod
	def get_excluded_files_list():
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'excluded_entities.txt'), 'r') as f:
			return f.read().splitlines()
