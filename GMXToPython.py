import xml.etree.ElementTree as ET
import os
from Element import Element

class GMXToPython(object):

	def __init__(self, xmlFile):
		self.gmxroot = ET.parse(xmlFile).getroot()
		self.root = Element(self.gmxroot)

		for child in self.gmxroot:
			self.process(child, self.root)

	def process(self, element, parent):
		elem = Element(element)
		elem.parent = parent
		parent.children.append(elem)
		elem.generation = parent.generation +1
		elem.generateCleanText()
		if elem.parent == self.root:
			elem.primogen = elem.tag
		else:
			elem.primogen = parent.primogen
		for child in element:
			self.process(child, elem)

