#!/usr/bin/python3

from sys import argv
from os import makedirs, symlink, listdir, remove, rmdir, removedirs
from os.path import abspath, join, split, exists, isfile, islink, realpath
from filecmp import dircmp, cmpfiles
from re import sub
from shutil import copy2, rmtree
from time import time

def extract(src_0, src_1):
	dircomp = dircmp(src_0, src_1) # 1 == Delete, 2 == Ignore
	for filename in dircomp.diff_files:
		yield (
			abspath(join(src_0, filename)),
			abspath(join(src_1, filename))
		)
	for filename in dircomp.right_only:
		yield (abspath(join(src_1, filename)), 1)
	for directory in dircomp.common_dirs:
		comparison = cmpfiles(
			src_0, src_1, listdir(src_0) + listdir(src_1),
			shallow = False)
		if len(comparison[1]) != 0:
			yield from extract(
				abspath(join(src_0, directory)),
				abspath(join(src_1, directory))
			)
		else:
			yield (directory, 2)

def size(src_1, total = 0):
	for name in listdir(src_1):
		path = join(src_1, name)
		if isfile(path): total += 1
		else: total = size(abspath(path), total)
	return total

def restore(file):
	total = size(file["source"])
	for current, oper in enumerate(extract(file["source"], file["restore"])):
		if oper[1] == 1: # delete
			try:
				remove(oper[0])
			except IsADirectoryError:
				rmtree(oper[0])
		elif oper[1] == 2: # skip
			continue
		source_file, destination_file = oper
		destination_file = sub(
			abspath(file["source"]),
			abspath(file["restore"]), source_file
		)
		destination = split(destination_file)[0]
		if not exists(destination):
			makedirs(destination)
		if isfile(destination_file):
			copy2(source_file, destination_file)
		print("\x1b[2K", f"{current/total:.0%} Complete", end = '\r')
	print("\x1b[2K", "100% Complete")

if __name__ == "__main__":
	true = lambda a, n: a[n] if a[n].endswith('/') else a[n] + '/'
	if len(argv) > 2:
		restore({"source": true(argv, 1),"restore": true(argv, 2)})
	else: print(
		f"Usage: {argv[0]} source_dir restored_dir"
	)



