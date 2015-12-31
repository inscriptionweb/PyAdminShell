import sys
import os
import config

class Action(object):

	def __init__(self, shell, name):
		super(Action, self).__init__()
		self._shell = shell
		self._name = name
		self._actions = {}

	def	execute(self, args=None):
		if not len(self._actions):
			do = getattr(self, "do", None)
			if callable(do):
				do(args)
			return
		if args and type(args) is list and len(args):
			action = args[0]
			if action in self._actions:
				self._actions[action](args[1:])
			else:
				self.usage()
		else:
			self.usage()

	def	usage(self):
		actions = ""
		for action in self._actions:
			if len(actions):
				actions += " |"
			actions += " " + action
		print("Usage : {0}{1}".format(self._name, actions))

	def	do(self):
		return

class ActionError(Exception):

	def __init__(self, value):
		self.value = "Action Error : " + value

	def __str__(self):
		return repr(self.value)

class ExitAction(Action):

	def __init__(self, shell):
		super(ExitAction, self).__init__(shell, "exit")

	def	do(self, args=None):
		if args:
			print("No arguments needed")
			return
		self._shell.isAlive = False
		sys.exit(0)

	def usage(self):
		self.do()

class HelpAction(Action):

	def __init__(self, shell):
		super(HelpAction, self).__init__(shell, "readme")

	def	do(self, args=None):
		if args and len(args) == 1:
			if args[0] in self._shell.actions:
				self._shell.actions[args[0]].usage()
				return
		elif args and len(args):
			self.usage()
			return
		print("Available actions :")
		for action in self._shell.actions:
			print("\t{0}".format(action))

	def	usage(self):
		print("Usage : help (action)")

class ConfigAction(Action):

	def __init__(self, shell):
		super(ConfigAction, self).__init__(shell, "config")
		self._actions = {"show": self.show,
						"modify": self.modify}
		self._confFiles = []
		self._rawFiles = []
		for item in os.listdir("./conf/"):
			self._rawFiles.append(item)
			self._confFiles.append(item.split(".")[0])

	def	show(self, args=None):
		if not args or len(args) != 1:
			for name in self._confFiles:
				print("\t{0}".format(name))
			return
		if args[0] not in self._confFiles:
			print("Config not available")
			return
		location = "./conf/" + self._rawFiles[self._confFiles.index(args[0])]
		if location.endswith(".json"):
			conf = config.Data(location)
		else:
			conf = config.Data(location, formatJson=False)
		print(conf.fancy())

	def	modify(self, args=None):
		if not args or len(args) not in (2, 3):
			print("Two arguments minimum")
			return
		if args[0] not in self._confFiles:
			print("Config not available")
			return
		location = "./conf/" + self._rawFiles[self._confFiles.index(args[0])]
		if location.endswith(".json"):
			conf = config.Data(location)
		else:
			conf = config.Data(location, formatJson=False)
		data = conf.get()
		if args[1] not in data:
			print("Key not available")
			return
		value = None if len(args) == 2 else args[2]
		conf[args[1]] = value
		conf.save()


def	getActions(shell):
	actions = {}

	actions["help"] = HelpAction(shell)
	actions["exit"] = ExitAction(shell)

	return actions
