from configparser import ConfigParser
from simple_term_menu import TerminalMenu

def setup(section):
	config = ConfigParser(inline_comment_prefixes = ('#', ';'))
	config.read("config.ini")
	dct = dict()
	for x, y in config[section.upper()].items():
		if ", " in y:
			dct[x] = y.split(", ")
		else:
			dct[x] = y
	return dct


def edit(config):
	result = ' '
	section = False
	while True:
		if section:
			lst = [".."] + [k for k in config[section]]
		else:
			lst = config.sections() + [' ', "Save & Exit", "Exit"]
		menu = TerminalMenu(lst)
		result = menu.show()
		if not result:
			return None
		result = lst[result]
		if result is ' ':
			continue
		elif result is "Save & Exit":
			return config
		elif result is "Exit":
			return None
		elif result is "..":
			section = False
		elif not section:
			section = result
		else:
			config[section][result] = key_edit(
				section, result, config[section][result]
			)

def in_filter(value):
	if ", " in value:
		lst = list()
		for v in value.split(", "):
			if "true" in value or "false" in value:
				lst.append(True if value is "true" else False)
			elif value.isdigit():
				lst.append(int(value))
			else:
				lst.append(value)
		return lst
	elif "true" in value or "false" in value:
		return True if value is "true" else False
	elif value.isdigit():
		return int(value)
	return value

def key_edit(section, key, value):
	print(f" [{section}]")
	value, comment = value.split(';')
	value = in_filter(value)
	if isinstance(value, list):
		menu = TerminalMenu(comment.split(' '))
		print(f" {key}", end = '\r')
		result = value[menu.show()]
		return input(f" {result}")
	else:
		print(f" {comment}")
		return input(f" {key}: ")
	

def modify():
	config = ConfigParser()
	config.read("config.ini")
	new_config = edit(config)
	print(new_config)



if __name__ == "__main__":
	modify()
