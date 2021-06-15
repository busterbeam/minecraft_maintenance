from configparser import ConfigParser

def setup(section):
	config = ConfigParser(inline_comment_prefixes = ('#', ';'))
	config.read("minecraft_maintenance.ini")
	dct = dict()
	for x, y in config[section.upper()].items():
		if ", " in y:
			dct[x] = y.split(", ")
		else:
			dct[x] = y
	return dct
