import os


class ProjectPath:
	
	@staticmethod
	def current_path():
		current_path = os.getcwd()
		return current_path

	@staticmethod
	def case_files_path():
		path = ProjectPath.current_path()
		case_files_path = path[:path.index("src") + len("src\\")] + "case_files\\"
		return case_files_path
