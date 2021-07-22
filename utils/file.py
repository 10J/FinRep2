"""
	# File Handling Utilities
	---------------------------------------------------------------------------
	Utility library for file and directory access.
	===========================================================================
"""

# Dependencies
import sys
import os

# Functions
def isDirectory( path ):
	return os.path.isdir( path )
	
def isFile( path ):
	return os.path.isfile( path )
	
def getDirectoryContents( path ):
	return os.listdir( path )
	
def readFile( path ):
	""" Read data from a file """
	data = ""
	if(isFile(path)):
		try:
			f = open( path, "r" )
			data = f.read()
			f.close()
		except:
			print("Unable to read file'",path,"'!")
	else:
		print("Provided path,'", path, "' isn't a valid file!")
	return data
	return
	
def writeFile( path, data ):
	""" Write data to a file """
	f = open( path, "w" )
	f.write(data)
	f.close()
	return