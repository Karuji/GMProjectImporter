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


def main():

	def findPrimogen(elem, string = ""):
		curElem = elem
		for i in range(elem.generation):
			if curElem.tag == "\'datafiles\'":
				string = str(curElem.attrib["name"]) + os.sep + string
			curElem = curElem.parent
		return string

	def process(elem, parent):
		#if elem.cleantext != "":
		#print(parent.tag + " | " + elem.tag + " : " + str(elem.attrib) + " ^ " + elem.cleantext + " % " + str(elem.generation))
		
		# if elem.tag == "\'name\'":
		# 	primogen = findPrimogen(elem)
		# 	print(primogen+elem.cleantext)

		for child in elem.children:
			print(child.tag)
			#process(child, elem)

	a = GMXToPython('C:\Dev\Games\zX-Hyperblast\Studio\zX_Hyperblast.gmx\zX_Hyperblast.project.gmx')
	process(a.root, a.root)

	


if __name__ == '__main__':
	main()