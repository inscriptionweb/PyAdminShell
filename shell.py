#!/usr/bin/python2.7

import signal
import sys
import shlex
import actions as SA

class Shell(object):

	def __init__(self):
		super(Shell, self).__init__()
		print("Welcome\n")
		signal.signal(signal.SIGINT, self.signal_handler)
		self.actions = SA.getActions(self)
		self.wemo = None
		self.twitter = None

	def	signal_handler(self, sig, frame):
		self.isAlive = False
		print("\nGoodbye!\b")
		sys.exit(0)

	def	launch(self):
		self.isAlive = True
		while self.isAlive:
			action = raw_input("$>")
			tmp = shlex.split(action)
			if len(tmp):
				actionName = tmp[0]
				args = tmp[1:]
				if actionName in self.actions:
					try:
						self.actions[actionName].execute(args)
					except Exception as e:
						print(str(e))
				else:
					print("Action {0} not found".format(actionName))
					self.actions["help"].execute()

if __name__ == '__main__':
	shell = Shell()
	shell.launch()
