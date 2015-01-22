import xml.etree.ElementTree as ET
import os
import shutil

class RawFile(object):
	def __init__(self, tag, xmlFile):
		self.fileName    = ""
		self.dirFileName = ""
		self.file = None

		if tag == ("\'sprite\'"):
			self.file = SprElement(xmlFile)
		if tag == ("\'background\'"):
			self.file = BgdElement(xmlFile)
		if tag == ("\'sound\'"):
			self.file = SndElement(xmlFile)
		if tag == ("\'font\'"):
			self.file = FntElement(xmlFile)

	def copyto(self, target):
		if self.file != None:
			self.file.copyto(target)

class RawElement(object):
	def __init__(self,  xmlFile):
		self.string = str(xmlFile)
		self.root = ET.parse(xmlFile).getroot()
		self.rawFiles = []
		self.splitName()

	def copyto(self, target):
		for raw in self.rawFiles:
			shutil.copyfile(self.string + raw, target + raw)

	def splitName(self):
		"""Splits the name into the FileName and extention."""
		pos = 0

		if os.sep in self.string:
			for i in range(1, len(self.string)):
				if self.string[-i] == os.sep:
					pos = i
					break
			self.string = self.string[:len(self.string)-pos]

class SprElement(RawElement):
	def __init__(self, xmlFile):
		super().__init__(xmlFile)
		for raw in self.root.iter('frame'):
			self.rawFiles.append(raw.text)

class BgdElement(RawElement):
	def __init__(self, xmlFile):
		super().__init__(xmlFile)
		for raw in self.root.iter('data'):
			self.rawFiles.append(raw.text)

class SndElement(RawElement):
	def __init__(self, xmlFile):
		super().__init__(xmlFile)
		for raw in self.root.iter('data'):
			self.rawFiles.append('audio'+os.sep+raw.text)

class FntElement(RawElement):
	def __init__(self, xmlFile):
		super().__init__(xmlFile)
		for raw in self.root.iter('image'):
			self.rawFiles.append(raw.text)
