'''
	Find & Replace Tool ( FinRep )
	---------------------------------------------------------------------------
	A tool for locating all instances of a regex pattern in code, generating a
	'patterns' file with each unique piece of code fitting that pattern, then 
	taking in the user-updated version of tha file ( a transform file ) and 
	performing the specified changes to each instance based on that transform
	file.
	===========================================================================
	Copyright Joseph Juma, C.M., Michael Maju 2021
'''

# Dependencies
import sys
import os
import re

import utils.file as fu
import utils.patterns as pu

# Functions
def displayHelp():
	'''
		Display a help message indicating how to use this.
	'''
	print("Example usage: 'finrep.py [config_file.frc]'")
	return

def loadConfigFile( path ):
	'''
		Load a finrep config file (*.frc).
	'''
	
	# Define some varibales
	dict = {}
	dict['ignore'] = []
	dict['pattern'] = []
	dict['transform'] = []
	data = None
	ld = None
	s = None
	
	data = fu.readFile(path)
	if( data != None ):
		data = data.split("\n")
		for line in data:
			ld = line.split(" ")
			s = ld[0]
			if(s == "#type"):
				# Type
				dict['type'] = ld[1]
			elif(s == "#path"):
				# input-file
				dict['path'] = ld[1]
			elif(s == "#pattern-file"):
				# pattern-file
				dict['patfile'] = ld[1]
			elif(s == "#i"):
				# ignore
				dict['ignore'].append(ld[1])
			elif(s == "#p"):
				# pattern
				dict['pattern'].append(' '.join(ld[1:]))
			elif(s == "#t"):
				# transform
				s = ' '.join(ld[1:])
				dict['transform'].append(s.split(' // '))
			else:
				# None of the above!
				s = []
	else:
		print("Error(loadConfigFile): cannot read file '",path,"'")
	return dict
		
def finrep( file ):
	'''
		Find & Replace logic!
	'''
	
	# Define some variables
	type = None
	regex = None
	ignore = []
	path = None
	patternsPath = "patterns.pat"
	
	# Load File
	config = loadConfigFile(file)
	
	if( config['type'] == "pattern" ):
		# Find Pattern
		pu.findPattern(config['pattern'][0],config['path'],'patterns.pat',config['ignore'])
	elif( config['type'] == "transform" ):
		# Replace Pattern
		pu.transformPatterns(config['transform'],config['path'])
	else:
		# Something else?
		print("Error: unable to parse provided file,'",file,"'.")
	return

# Main
if __name__ == "__main__":
	if( len(sys.argv[1:]) < 1 ):
		print("Error: too few parameters passed.")
		displayHelp()
	else:
		finrep( sys.argv[1] )