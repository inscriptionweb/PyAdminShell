import json

class Data(object):

	def __init__(self, filename, formatJson=True):
		super(Data, self).__init__()
		self._filename = filename
		self._formatJson = formatJson
		self._read()

	def	__str__(self):
		return json.dumps(self._json)

	def	__getitem__(self, key):
		self._read()
		if key in self._json:
			return self._json[key]
		return None

	def	__setitem__(self, key, value):
		self._json[key] = value
		self._write()

	def	_read(self):
		with open(self._filename) as _file:
			self._rawData = _file.read()
			if not self._formatJson:
				self._rawData = "{\"" + self._rawData.replace("\r", "").replace("\n\n", "\n").replace("=", "\":\"").replace("\n", "\",\n\"").replace(",\n\"\"", "") + "\"}"
			self._json = json.loads(self._rawData)

	def	_write(self):
		with open(self._filename, "w") as _file:
			self._rawData = json.dumps(self._json)
			if not self._formatJson:
				self._rawData = self._rawData.replace("{", "").replace("}", "").replace("\"", "").replace(": ", "=").replace(", ", "\n")
			_file.write(self._rawData)

	def	load(self):
		self._read()

	def	save(self):
		self._write()

	def	get(self):
		return self._json

	def	set(self):
		return self._json

	def	fancy(self):
		out = ""
		isFirst = True
		for key in self._json:
			out += "{2}{0} => {1}".format(key, self._json[key],"\n" if not isFirst else "")
			isFirst = False
		return out

class	Error(Exception):

	def __init__(self, value):
		self.value = "Config Error : " + value

	def __str__(self):
		return repr(self.value)