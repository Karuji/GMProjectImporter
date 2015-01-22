class Element(object):

	def _initVar(self):
		self.tag        = ""
		self.attrib     = {}
		self.text       = ""
		self.cleantext  = ""
		self.primogen   = ""
		self.parent     = None
		self.children   = []
		self.generation = 0
		self.filename   = ""
		self.taglist    = []
		self.filelist   = []

		self.taglist.append("\'sound\'")
		self.taglist.append("\'sprite\'")
		self.taglist.append("\'background\'")
		self.taglist.append("\'object\'")
		self.taglist.append("\'room\'")
		self.taglist.append("\'trigger\'")
		self.taglist.append("\'font\'")

		self.filelist = self.taglist.copy()
		self.filelist.append("\'name\'")
		self.filelist.append("\'script\'")

	def _validate(self):
		if self.text[:3] == "\'\\n":
			self.cleantext = ""
		else:
			self.cleantext = self.text

	def generateCleanText(self):
		if self.cleantext == None:
			cleantext = ""
		if self.parent != None:
			if self.parent.tag == "\'datafile\'":
				if self.tag != "\'name\'":
					self.cleantext = ""
			elif self.parent.tag == "\'Config\'":
				if self.tag == "\'CopyToMask\'":
					self.cleantext = ""

		if self.cleantext != "":
			if self.tag in self.filelist:
				self.cleantext = self.cleantext.replace("\'","")
				if self.tag in self.taglist:
					txt = self.tag.replace("\'", "")
					self.cleantext += "." + txt + '.gmx'
			else:
				self.cleantext = ""

	def __init__(self, xml=None):
		self._initVar()
		if xml is not None:
			self.tag = repr(xml.tag)
			self.attrib = xml.attrib
			self.text = repr(xml.text)
			self._validate()
