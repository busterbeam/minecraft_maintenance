#!/usr/bin/python3

from sys import argv
from os import makedirs, symlink, listdir
from os.path import abspath, join, split, exists, isfile, islink, realpath
from filecmp import dircmp, cmpfiles
from re import sub
from shutil import copy2, copytree
import shutil
from time import time

shutil._samefile = lambda *a, **k: False

def compare(src_0, src_1):
	dircomp = dircmp(src_0, src_1)
	for filename in dircomp.same_files:
		yield (abspath(join(src_0, filename)), False)
	for filename in dircomp.right_only + dircomp.diff_files:
		yield (abspath(join(src_0, filename)), True)
	for directory in dircomp.common_dirs:
		comparison = cmpfiles(
			src_0, src_1, listdir(src_0) + listdir(src_1),
			shallow = False)
		if len(comparison[1]) != 0:
			yield from compare(
				abspath(join(src_0, directory)),
				abspath(join(src_1, directory))
			)
		else:
			yield (directory, False)

def size(src_1, total = 0):
	for name in listdir(src_1):
		path = join(src_1, name)
		if isfile(path): total += 1
		else: total = size(abspath(path), total)
	return total

global CURRENT_TOTAL
CURRENT_TOTAL = 0
def copytree_print(_, names, total):
	CURRENT_TOTAL += len(names)
	print(
		"\x1b[2K",
		f"{CURRENT_TOTAL/total:.0%} Complete",
		end = '\r'
	)

def backup(file, _type = "diff"):
	total = size(file["dest"])
	if _type is "full":
		copytree(
			file["dest"], file["new"],
			ignore = lambda s, n: copytree_print(s, n, total)
		)
		CURRENT_TOTAL = 0
		symlink(file["new"], "latest")
		return
	for current, src_n_diff in enumerate(compare(file["src"], file["dest"])):
		source_file, differ = src_n_diff
		destination_file = sub(
			abspath(file["src"]), abspath(file["new"]), source_file)
		destination = split(destination_file)[0]
		if not exists(destination):
			makedirs(destination)
		if not differ:
			if islink(source_file):
				symlink(realpath(source_file), destination_file)
			elif isfile(source_file) and not islink(destination_file):
				symlink(source_file, destination_file)
		elif isfile(source_file):
			if not copy2(source_file, destination_file):
				print(source_file, destination_file)
		print("\x1b[2K", f"{current/total:.0%} Complete", end = '\r')
	symlink(file["new"], "latest")
	print("\x1b[2K", "100% Complete")

if __name__ == "__main__":
	true = lambda a, n: a[n] if a[n].endswith('/') else f"{a[n]}/"
	if len(argv) > 3:
		backup(
			{"src": true(argv,1), "dest": true(argv,2), "new": true(argv,3)}
		)
	else:
		print(f"Usage: {argv[0]} prev_dir source_dir difference_dir")



