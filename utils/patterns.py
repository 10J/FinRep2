"""
	# Patterns Utility Library
	---------------------------------------------------------------------------
	A collection of utility functions for working with regex related patterns,
	and pattern-strings.
	===========================================================================
"""

# Dependencies
import re
import utils.file as fu

# Functions

# Pattern Finding Utilities
def searchForPattern( regex, str ):
	"""
		## Search For Pattern
		-----------------------------------------------------------------------
		Search a given string for all instances of a provided pattern. Returns
		a list of start-end position pairs for each instance of the pattern 
		found within the string.
		=======================================================================
	"""
	
	# Define some variables
	data = []
	index = 0
	
	# Until we reach the end of the file,
	while (index < len(str)):
		# Search for the pattern,
		match = regex.search(str,index)
		
		# If the pattern is found,
		if( match != None):
			span = match.span()	# Get the start and end of the group matched,
			data.append(str[span[0]:span[1]])	# Get the substring between the match positions
			index = span[1]	# Set i to the end of the match so an infinite loop is avoided
		# Else, if a pattern isn't found,
		else:
			# Safely break the loop
			index = len(str)
			break
	
	return data

def generateRegexFromPattern( pattern ):
	"""
		## Generate Regex from Pattern
		-----------------------------------------------------------------------
		Generates a regex object from a provided pattern string.
		=======================================================================
	"""
	
	return re.compile(pattern)

def getFilesInDirectory( path, ignore = [] ):
		"""
			## Get Files in Directory
			-------------------------------------------------------------------
			Move through each file in and sub-directory within a given path,
			and return a list of every file within them.
			===================================================================
		"""
		
		# Define some variables
		files = []
		
		# If the path is to be ignored, ignore it!
		if path in ignore:
			return[]
		# Else, if I shouldn't ignore it,
		else:
			# If the path is a directory,
			if(fu.isDirectory(path)):
				objects = fu.getDirectoryContents(path) # Get the contents of the directory,
				# For each object in the directory,
				for object in objects:
					p = path + "\\" + object # Construct a new path
					files.extend(getFilesInDirectory(p,ignore))	# Then call this function on that path! Recursion~
				return files	# When you're all done, return all the files you got this way.
			# Else, If the path is a file,
			elif(fu.isFile(path)):
				files.append(path) # Add it to the files list,
				return files # Then return that list!
			# Else, if it's none of those, what is it? Return empty!
			else:
				return []
				
def findPattern( pattern, path, outputPath = "patterns.pat", ignore = [] ):
	"""
		## Find Pattern
		-----------------------------------------------------------------------
		Given a pattern, and a directory path:
			1.	Construct a regex pattern,
			2.	Search files in the given directory using regex,
			3.	If a pattern is found that doesn't already match a string in 
				the list, add it to the list.
			4.	Write the list of pattern-strings to the file in a serialized
				format.
		=======================================================================
	"""
	
	# Define some variables
	rgx = None
	patterns = []
	
	# Construct the ReGeX from the pattern-string
	rgx = generateRegexFromPattern(pattern)
	
	# Traverse the directory for a list of files
	files = getFilesInDirectory( path, ignore )
	
	# If files were returned,
	if(len(files) != 0 ):
		# For each file found,
		for file in files:
			data = fu.readFile(file)	# Read the file into a string
			patterns.extend(searchForPattern(rgx,data))	# Get pattern matching strings
		patterns = list(set(patterns))	# Some ol type conversion
		fu.writeFile( outputPath, ("\n".join(patterns)))	# Write pattern-matching strings to file
	
	# Else, if no files were returned,
	else:
		# Error
		print("Error(findPattern): Path provided is not a valid file or directory path.")
	
	# Return
	return

# Pattern Transformation Utilities	
def replacePattern( pattern, str ):
	"""
		## Replace Pattern
		-----------------------------------------------------------------------
		Given a string and single pattern, replace all instances of that 
		pattern found in the string!
		=======================================================================
	"""
	
	# Do the thing~
	try:
		return str.replace(pattern[0],pattern[1])
	except:
		print("Error(replacePattern): Invalid transform syntax on pattern,",pattern[0],"! Skipping...")
		return str

def replacePatterns( patterns, str ):
	"""
		## Replace Patterns
		-----------------------------------------------------------------------
		Given a string and patterns, replace the matching ones found in the 
		string.
		=======================================================================
	"""
	
	# Make a copy of the string so we don't get weird behavior~
	s = str
	
	# For each pattern,
	for pattern in patterns:
		s = replacePattern(pattern,s)	# Replace the pattern
	return s
	
def transformPatternsFile( transforms, filePath ):
	"""
		## Transform Patterns File
		-----------------------------------------------------------------------
		Given a path to a specific file and a list of pattern-transforms, 
		execute those transforms on pattern-matching substrings in the file.
		=======================================================================
	"""
	
	str = fu.readFile(filePath)	# Read the file
	data = replacePatterns(transforms,str)	# Replace matching patterns in the file data
	
	# If the file data was updated,
	if( str != data ):
		fu.writeFile( filePath, data )	# Write the file data output
	return
	
def transformPatterns( transforms, dir ):
	"""
		## Transform Patterns
		-----------------------------------------------------------------------
		Recursively go through a directory and transform pattern-strings,
		based on a transform file schema.
		=======================================================================
	"""
	
	# Get files in the given directory,
	files = getFilesInDirectory(dir)
	
	# If files were gotten,
	if( len(files) != 0 ):
		# For each file,
		for file in files:
			# Transform the file
			transformPatternsFile(transforms,file)
	# Else, if no files were gotten,
	else:
		print("Error( transformPatterns ): Path provided is not a valid directory of file path.")
	return
	