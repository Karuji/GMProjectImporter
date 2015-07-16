import sys
from cx_Freeze import setup, Executable

setup(
    name = "GMProjectImporter",
    version = "0.l",
    description = "Program for the bulk renaming of files in an ordered manner",
    executables = [Executable("GMProjectImporter.py", base = "Console")])