import os


def get_all_files(filetype, folder, use_p4=False):
	"""Get all the files to parse returns an array of paths"""
	file_paths = list()
	for root, dirs, files in os.walk(folder):
		for f in files:
			if f.endswith(filetype):
				file_paths.append(os.path.join(root, f))
	if use_p4:
		from P4 import P4
		p4 = P4()
		p4.exception_level = 1
		p4.client = ''
		p4.user = ''
		p4.port = ''
		p4.connect()
		return p4.run('fstat', file_paths)

	else:
		return file_paths
