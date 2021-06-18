from subprocess import run

server_name = "mc-server"
mc_command = f"screen -S {server_name} -X stuff"

def command(cmd):
	return run([
		"screen", "-S", server_name,
		"-X", "stuff", f"'{cmd}'^M"
	])

def title(message, **kwargs):
	kwargs["text"] = message
	kwargs = sub("'", '"', str(kwargs))
	return command(f"title @a title {kwargs}")

def print(message):
	QU = '\"'
	if isinstance(message, (dict, list)):
		message = sub("'", '"', str(message))
		return command(
			f"title @a actionbar {message}"
		)
	else:
		return command(
			f"title @a actionbar {QU}{message}{QU}"
		)

def playsound(sound, pitch = 2, volume = 1):
	return command(
		"playsound {sound} master @a ~ ~ ~ {pitch} {volume}"
	)

class BossBar(Process):
	def __init__(self, *args, **kwargs):
		self.screen = mc_command
		self.name = f"server_maintance:{kwargs.get('name', 'boss_bar')}"
		self.total = int(kwargs.get("total", 100))
		self.colour = kwargs.get("color", "white")
		self.current = 0
		self.bar_set = True

	def __add__(self, num):
		if not self.bar_set:
			raise Exception("Bar not set")
		self.current += num

	def set(self, value):
		if not self.bar_set:
			raise Exception("Bar not set")
		self.current = value

	def run(self):
		""" The loop to keep the bossbar updated """
		while self.bar_set:
			sleep(1/3)
			command(f"bossbar set {self.name} value {self.current}")

	def __enter__(self):
		""" start boss bar """
		command(f"bossbar add {self.name} {QU}{title}{QU}")
		command(f"bossbar set {self.name} max {self.size}")
		command(f"bossbar set {self.name} players @a")
		self.start()
		return self

	def update(self, value):
		self.__add__(value)

	def __exit__(self):
		""" close boss bar """
		self.bar_set = False
		command(f"bossbar remove {self.name}")
