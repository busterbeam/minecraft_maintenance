#!/usr/bin/python3

from sys import argv
from os import listdir
from os.path import abspath, join, split, isfile, islink, isdir
from time import time, strftime
from config import setup

def size(src_0, total = 0):
	for name in listdir(src_0):
		path = join(src_0, name)
		if isfile(path):
			total += 1
		else:
			total = size(abspath(path), total)
	return total

def list_directory(directory, ignore):
	for name in listdir(directory):
		path = join(directory, name)
		if ignore in path:
			continue
		elif isfile(path):
			yield abspath(path)
		else:
			yield from list_directory(abspath(path), ignore)

def zipper(base_name, directory, config):
	comp_lvl = 9 if config["level"] == "default" else config["level"]
	from zipfile import ZipFile, ZIP_LZMA, ZIP_BZIP2, ZIP_DEFLATED, ZIP_STORED
	comp = eval((config["method"].replace('.', '_')).upper())
	with ZipFile(f"{base_name}.zip", 'w', comp, True, int(comp_lvl)) as zip_file:
		for filename in list_directory(directory, config["ignore"]):
			yield zip_file.write(filename)

def tarrer(base_name, directory):
	comp = config["method"].split('.')[1]
	comp_lvl = int(config["level"])
	from tarfile import open
	with open(base_name, f"w:{comp}", compresslevel = comp_lvl) as tar_file:
		for filename in list_directory(directory, config["ignore"]):
			yield tar_file.add(filename)

def archive(directory):
	total = size(directory)
	config = setup("archive")
	path = config["path"]
	if config["persistance"]:
		base_name = f"{path}/{strftime('%Y_%m_%d')}_archive"
	else:
		for i, name in enumerate(["daily", "weekly", "monthly", "quartly"]):
			if config['regularity'][i] == 3: # current time
				base_name = f"{path}/{name}_archive"
	if "zip" in config["method"].split('.')[0]:
		for i, _ in enumerate(zipper(base_name, directory, config)):
			print("\x1b[2K", f"{i/total:.0%} Complete", end = '\r')
	else:
		for i, _ in enumerate(tarrer(base_name, directory, config)):
			print("\x1b[2K", f"{i/total:.0%} Complete", end = '\r')
	print("\x1b[2K", "100% Complete")

if __name__ == "__main__":
	true = lambda a, n: a[n] if a[n].endswith('/') else f"{a[n]}/"
	if len(argv) > 0:
		archive(true(argv,1))
	else:
		print(f"Usage: {argv[0]} dir_to_archive")
