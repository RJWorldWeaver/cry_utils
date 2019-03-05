import os


def get_excluded_files():
	with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'excluded_entities.txt'), 'r') as f:
		return f.read().splitlines()
