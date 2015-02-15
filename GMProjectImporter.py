from GMXToPython import GMXToPython
from PythonToGMX import PythonToGMX
from RawElement import *
import xml.etree.ElementTree as ET
import os
import xml.dom.minidom
import shutil
import sys
import msvcrt

#import osnav
class Importer(object):
	def __init__(self):
		self._initVar()

		if self.getInput():

			self.sourcedir = self.getDir(self.sourceGMX) + os.sep
			self.targetdir = self.getDir(self.targetGMX) + os.sep

			self.source = GMXToPython(self.sourceGMX)
			self.target = GMXToPython(self.targetGMX)

			# Merge files

			self.merge()

			# Output to target

			self.writeMergedGMX()

			#copy files in GM directories

			self.copyFiles(self.source.root)
			self.copyTrees()


	def getInput(self):
		print("""GMProjectImporter

Copyright (c) 2015 Julian Pritchard

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.""")

		print("""\n\nSecond Disclaimer:
This program is a functional prototype.
It is likely that there are bugs and glitches, and things might break...
HORRIBLY.
For your own sanity please use version control or make a backup of your project\n""")

		var = input("Do you have a backup of your project? (Y/N): ")
		var = var.lower()
		if var[0] == 'y':
			print("Just remember you said you had a backup!\n")
			print("You can type exit to exit")
			print("You will need to a completely directory to the .project.gmx file")
			print("You should be entering something like:")
			print("C:\\GameDev\\MyCoolGame\\MyCoolGame.gmx\\MyCoolGame.project.gmx")
			source = input("Enter source for insert: ")
			if source.lower == 'exit':
				print("User want program to stop. Ok.")
				return False
			if '.project.gmx' not in source:
				print("This doesn't look like a .project.gmx program will now hide from user")
				return False
			else:
				target = input("Target to insert source into: ")
				if target.lower() == 'exit':
					print("Don't worry, it's me, not you")
					return False
				if '.project.gmx' not in target:
					print("Program is scared of files that aren't .project.gmx")
					print("Press any key to exit")
					return False
				else:
					self.sourceGMX = source
					self.targetGMX = target
					return True
		else:
			print("Go make a back up, or add your project to version control\nThen we can talk")
			return False

	def _initVar(self):
		self.ignoredTags = []
		self.rawfilegmx  = []
		self.hasrawfile  = []
		self.taglist     = []
		self.dircopy     = []
		self.treecopy    = []

		self.ignoredTags.append("\'Configs\'")
		self.ignoredTags.append("\'help\'")
		self.ignoredTags.append("\'TutorialState\'")

		self.hasrawfile.append("\'sprite\'")
		self.hasrawfile.append("\'background\'")
		self.hasrawfile.append("\'sound\'")
		self.hasrawfile.append("\'font\'")

		self.taglist.append("\'Configs\'")
		self.taglist.append("\'help\'")
		self.taglist.append("\'TutorialState\'")
		self.taglist.append("\'sound\'")
		self.taglist.append("\'sprite\'")
		self.taglist.append("\'background\'")
		self.taglist.append("\'object\'")
		self.taglist.append("\'room\'")
		self.taglist.append("\'trigger\'")
		self.taglist.append("\'font\'")

	def getDir(self, string):
		string = string.replace('.project.gmx', '')
		pos = 0

		if os.sep in string:
			for i in range(1, len(string)):
				if string[-i] == os.sep:
					pos = i
					break
			string = string[:len(string)-pos]
		return string

	def merge(self):
		for _1stgen in self.source.root.children:
			if _1stgen.tag not in self.ignoredTags:
				bIndex = self.findRootElementIndex(self.target.root, _1stgen.tag)
				for _2ndgen in _1stgen.children:
					if bIndex != -1:
						self.target.root.children[bIndex].children.append(_2ndgen)

	def copyFiles(self, elem):		
		if elem.cleantext != "":
			if elem.tag != "\'name\'":
				# You're checking a descendant tag again a primogen
				if self.findRootElementIndex(self.target.root, elem.primogen) != -1:
					shutil.copyfile(self.sourcedir+elem.cleantext, self.targetdir + elem.cleantext)
					if elem.tag in self.hasrawfile:
						raw = RawFile(elem.tag, self.sourcedir + elem.cleantext)
						rawfiledir = elem.tag.replace("\'","")
						if rawfiledir != "sound":
							rawfiledir += "s" + os.sep
						raw.copyto(self.targetdir+rawfiledir)
				else:
					print(elem.tag,elem.cleantext)
					self.treeCopyAdd(elem.tag)
		for child in elem.children:
			self.copyFiles(child)

	def treeCopyAdd(self, tag):
		print(self.treecopy)
		tag = tag.replace("\'", "")
		if tag not in self.treecopy:
			self.treecopy.append(tag)

	def copyTrees(self):
		if self.findRootElementIndex(self.source.root, "\'datafiles\'") != -1:
			self.treecopy.append('datafile')
			for branch in self.treecopy:
				if branch != 'sound':
					branch += 's'
				shutil.copytree(self.sourcedir + branch, self.targetdir + branch)

	def findRootElementIndex(self, root, tag):
		result = -1
		for child in root.children:
			if child.tag == tag:
				return root.children.index(child)
		return result

	def findPrimogen(self, elem, string = ""):
		curElem = elem
		for i in range(elem.generation):
			if curElem.tag == "\'datafiles\'":
				string = str(curElem.attrib["name"]) + os.sep + string
			curElem = curElem.parent
		return string

	def writeMergedGMX(self):
		gmxroot = PythonToGMX(self.target.root).root
		gmx = xml.dom.minidom.parseString(ET.tostring(gmxroot))
		pretty_xml_as_string = gmx.toprettyxml()
		gmxfile = open(self.targetGMX,'w')
		gmxfile.write(pretty_xml_as_string)
		gmxfile.close()
		gmxfile = open(self.targetGMX,'r')
		lines = gmxfile.readlines()
		gmxfile.close()
		if lines[0] != "<assets>":
			lines[0] = "<!--This Document is generated by GameMaker, if you edit it by hand then you do so at your own risk!-->\n"
		gmxfile = open(self.targetGMX,'w')
		for line in lines:
			line = line.expandtabs(2)
			if line.rstrip():
				gmxfile.write(line)
		gmxfile.close

def main():
	importer = Importer()

if __name__ == '__main__':
	main()
	