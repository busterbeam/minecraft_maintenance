#!/usr/bin/python3

from sys import argv
from subprocess import run
from os import chdir, system, listdir
from re import sub
from hashlib import sha256
from datetime import datetime
from requests import get
from time import sleep, time, time_ns, localtime
from prompt import command, playsound, BossBar, title
from configparser import ConfigParser

def setup():
	config = ConfigParser()
	config.read("minecraft_maintenance.ini")
	return config

QU = '\"'


def download(version, build, name):
	""" """
	with get(url(version, build, name), stream = True) as response:
		response.raise_for_status()
		if not response.ok:
			return False
		kwargs = {
			"name": "Downloading Update {version} {build}"
			"total": response.headers["Content-Length"]
		}
		with BossBar(**kwargs) as bb:
			with open(name, "wb") as jar_file:
				for chunk in response.iter_content(4096):
					if chunk:
						jar_file.write(chunk)
						bb += chunk


class Main:
	def __init__(self, *args, **kwargs):
		server_path = kwargs.get("server_path", '.')
		chdir(server_path)
		backup_path = kwargs.get("backup_path", False)
		if not backup_path:
			raise Exception("Backup Path must be provided")
		self.name = self.find_jar()
		_, self.version, build = self.name.split('-')
		self.build = build.rstrip('.jar')
		self.server_api = "https://papermc.io/api/v2/projects/paper"
		self.sha256 = self.server_hash()
		if not "mc-server" in run(["screen", "-list"], capture_output = True):
			self.start()
		self.backup()
	
	def find_jar(self):
		for filename in listdir():
			if filename.endswith(".jar"):
				return filename
	
	def timer(self, seconds):
		start = time_ns()
		end = start + (seconds * 10**6)
		with BossBar(total = seconds * 10**6) as bb:
			while time_ns() < end:
				if 4.9*10**6 < (end - time_ns()) < 5.1*10**6:
					playsound("block.note_block.iron_xylophone")
					print(" 5 Seconds Remaining!!")
				bb.set(start - time_ns())
	
	def start(self):
		system(
			f"screen -dmS mc-server java -Xms1G -Xmx4G -d64 -jar {self.name} -nogui"
		)
	
	def stop(self):
		title("Server Stopping Now!")
		command("stop")
	
	def update(self, server_path, backup_path):
		update = self.check_update()
		if update:
			print("You have 1 minute to finish what your doing")
			backup({
				"src": f"{backup_path}/latest/",
				"dest": f"{server_path}/",
				"new": f"{backup_path}/temporary/"
			}) # temporary backup
			download(version, build, download_name)
			self.timer(60)
			self.stop()
	
	def backup(self, server_path, backup_path):
		hour = localtime().tm_hour
		wday = localtime().tm_wday
		mday = localtime().tm_mday
		file = {
			"src": f"{backup_path}/latest/", "dest": f"{server_path}/",
			"new": "{backup_path}/{strftime('%Y_%m_%d')}/"}
		if hour == self.mon_time and mday == self.mon_day:
			backup(file, "full") # monthy
		elif hour == self.week_time and wday == self.week_day:
			backup(file) # weekly
		elif hour == self.daily_time:
			backup(file) # daily
		else: # hourly overides itself
			file["new"] = "{backup_path}/hourly_{strftime('%H')}/"
			backup(file) # hourly
	
	def server_hash(self):
		sha256_hash = sha256()
		with open(self.name, 'rb') as server_file:
			for byte_block in iter(lambda: server_file.read(4096), b''):
				sha256_hash.update(byte_block)
		return sha256_hash.hexdigest()
	
	def check_update(self):
		print("Checking for updates")
		version = (get(url()).json())["versions"][-1]
		build = (get(url(version)).json())["builds"][-1]
		dct = get(url(version, build)).json()
		name = dct["downloads"]["name"]
		new_sha256 = dct["downloads"]["sha256"]
		if version > self.version and new_sha256 != self.sha256:
			print(
				f"There is a new version!  With the changes {dct['message']}",
				f"In summary the update does {dct['summary']}")
			return (version, build, name)
		elif build > self.build and new_sha256 != self.sha256:
			print(
				f"There is a new build!  With the changes {dct['message']}",
				f"In summary the update does {dct['summary']}")
			return (version, build, name)
		else:
			print("No new update found")
			return False
	
	def url(self, *args):
		server_api = self.server_api
		if len(args) < 1:
			return f"{server_api}"
		elif len(args) < 2:
			return f"{server_api}/versions/{args[0]}"
		elif len(args) < 3:
			return f"{server_api}/versions/{args[0]}/builds/{args[1]}"
		return f"{server_api}/versions/{args[0]}/builds/{args[1]}/downloads/{args[2]}"




if __name__ == "__main__":
	if argv[1] == "restore":
		Main("restore")
	
	settings = setup()
