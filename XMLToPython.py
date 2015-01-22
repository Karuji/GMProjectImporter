import xml.etree.ElementTree as ET
import os
from FileName import FileName

class ElementFile(FileName):
	self.location = ""

class Element(object):
	tag        = ""
	attrib     = ""
	text       = ""
	parent     = None
	children   = []
	generation = 0
	filename   = None

class XMLToPython(object):

	def __init__(self, xmlFile):
		self.root = ET.parse(xmlFile).getroot()
