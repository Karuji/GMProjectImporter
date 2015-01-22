import xml.etree.ElementTree as ET
import os
from Element import Element

class PythonToGMX(object):

	def __init__(self, pythonTree):
		self.pythonroot = pythonTree
		self.root = ET.Element(eval(self.pythonroot.tag))

		for child in self.pythonroot.children:
			self.process(child, self.root)

	def process(self, element, parent):
		elem = ET.SubElement(parent, eval(element.tag), element.attrib)
		elem.text = eval(element.text)
		for child in element.children:
			self.process(child, elem)
