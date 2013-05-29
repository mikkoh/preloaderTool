import json
import os
import sys
from optparse import OptionParser



class ScreenPrinter:
	BLACK = 'BLACK'
	RED = 'red'
	GREEN = 'green'
	YELLOW = 'yellow'
	BLUE = 'blue'
	MAGENTA = 'magenta'
	CYAN = 'cyan'
	WHITE = 'white'

	curFore = 39
	curBG = 49
	doBold = False
	doBlink = False
	doUnderline = False

	def setForeground( self, colour = 'NONE' ):
		if colour == self.BLACK:
			self.curFore = 30
		elif colour == self.RED:
			self.curFore = 31
		elif colour == self.GREEN:
			self.curFore = 32
		elif colour == self.YELLOW:
			self.curFore = 33
		elif colour == self.BLUE:
			self.curFore = 34
		elif colour == self.MAGENTA:
			self.curFore = 35
		elif colour == self.CYAN:
			self.curFore = 36
		elif colour == self.WHITE:
			self.curFore = 37
		else:
			self.curFore = 39

	def setBackground( self, colour = 'NONE' ):
		if colour == self.BLACK:
			self.curBG = 40
		elif colour == self.RED:
			self.curBG = 41
		elif colour == self.GREEN:
			self.curBG = 42
		elif colour == self.YELLOW:
			self.curBG = 43
		elif colour == self.BLUE:
			self.curBG = 44
		elif colour == self.MAGENTA:
			self.curBG = 45
		elif colour == self.CYAN:
			self.curBG = 46
		elif colour == self.WHITE:
			self.curBG = 47
		else:
			self.curBG = 49

	def o( self, msg ):
		sys.stdout.write( self.getEscape() + msg + '\x1b[0m' )

	def out( self, msg ):
		print self.getEscape() + msg + self.getReset()

	def outReset( self ):
		sys.stdout.write( '\x1b[0m' )		

	def getEscape( self ):
		escape = '\x1b[' + str( self.curFore ) + ";" + str( self.curBG );

		if self.doBold:
			escape += ';1'
		
		if self.doBlink:
			escape += ';5'

		if self.doUnderline:
			escape += ';4'


		escape += 'm';

		return escape

	def getReset( self ):
		return '\x1b[0m'




# this function will be used to traverse json and look for img tags
def lookForImg( data, listToAddTo, jsonTags ):
	if isinstance( data, dict ):
		for key in data:			
			for jsonTag in jsonTags:
				if key == jsonTag and isinstance( data[ key ], unicode ):
					listToAddTo.append( { 'url': data[ key ], 'type': jsonTag } )
				elif isinstance( data[ key ], list ) or isinstance( data[ key ], dict ):
					lookForImg( data[ key ], listToAddTo, jsonTags )

	elif isinstance( data, list ):
		for item in data:
			lookForImg( item, listToAddTo, jsonTags )


def getDataForJSONPath( jsonData, path ):
	try:
		rVal = jsonData

		pathSplit = path.rsplit( '.' )
		length = len( pathSplit )

		for i in range( 0, length ):
			pathPart = pathSplit[ i ]
			
			if pathPart.isdigit():
				rVal = rVal[ int( pathPart ) ]
			else:
				# since it exists we continue to traverse as normal
				if pathPart in rVal:
					rVal = rVal[ pathPart ]
				# since it doesnt exist we'll add it
				else:
					if i + 1 < length:
						nextPathPart = pathSplit[ i + 1 ]

						if nextPathPart.isdigit:
							rVal[ pathPart ] = []
						else:
							rVal[ pathPart ] = {}
					else:
						rVal[ pathPart ] = {}

					rVal = rVal[ pathPart ]

			# if we're on the last item we want to check if we have a retina 
			# and regular load object
			if i == length - 1:
				if 'regular' not in rVal:
					rVal[ 'regular' ] = []

				if 'retina' not in rVal:
					rVal[ 'retina' ] = []

		return rVal
	except:
		 printer.setForeground( printer.RED )
		 printer.out( 'YOUR JSON PATH MAYBE INCORRECT' )





try:
	printer = ScreenPrinter();
	printer.setBackground( printer.CYAN )
	printer.setForeground( printer.CYAN )
	printer.o( '\n\n\n       \n' )
	printer.o( '  ' )
	printer.setBackground()
	printer.o( '   ' )
	printer.setBackground( printer.CYAN )
	printer.o( '  \n' )
	printer.o( '       \n' )
	printer.o( '  \n' )
	printer.o( '  \n' )
	printer.o( '  ' )
	printer.setBackground()
	printer.doBold = True
	printer.o( ' RELOADER HELPER\n\n\n' )
	printer.setForeground()
	printer.setBackground()

	jsonExampleData = [];
	jsonExampleData.append( {} );
	jsonExampleData[ 0 ][ 'filesToPreload' ] = [];
	jsonExampleData[ 0 ][ 'filesToPreload' ].append( { 'url': 'urlToItem1.jpg' } );
	jsonExampleData[ 0 ][ 'filesToPreload' ].append( { 'url': 'urlToItem2.jpg' } );

	jsonExample = json.dumps( jsonExampleData, indent=4, separators=(',', ': ') )

	printer.setForeground( printer.YELLOW )
	usage =  ( "usage: %prog " + printer.getEscape() + "jsonInput" + printer.getReset() + " " + printer.getEscape() + "jsonOutput" + printer.getReset() + " " + printer.getEscape() + "jsonAssetPath" + printer.getReset() + " [options]\n"
			   "\n\n" + printer.getEscape() + "jsonInput" + printer.getReset() + ":\nIs a path to a file that will be parsed for asset files eg. ./inputJSON.json"
			   "\n\n" + printer.getEscape() + "jsonOutput" + printer.getReset() + ":\nIs the path that the preload information will be output into eg. ./outputJSON.json"
			   "\n\n" + printer.getEscape() + "jsonAssetPath" + printer.getReset() + ":\nIs an array where input files could exist and is where the preloader data will be in the output. Array indices should be donated by the numeric index. eg. 0.filesToPreload (at index 0 variable filesToPreload) if your json looked like:\n" + jsonExample )

	cmdParser = OptionParser(usage=usage);
	cmdParser.add_option( "--cwd", dest="cwd", default="./", help="Base path for asset files", metavar="ASSET_FOLDER" )
	cmdParser.add_option( "--urlTags", dest="urlTags", default="img,video,audio", help="Define json tag names for urls for assets using a comma separated list eg. img,video,audio" )
	cmdParser.add_option( "-p", action="store_true", dest="parse", help="Adding this option in will make it so that the json will be parsed for images" )
	cmdParser.add_option( "-i", action="store_true", dest="interactiveParse", help="Use this option to interactively add items if we're parsing" )
	cmdParser.add_option( "--pretty", action="store_true", dest="pretty", help="If you'd like the output to be pretty printed use this option" )

	(options, args) = cmdParser.parse_args()


	# this is where all the magic will start to happen
	if len( args ) < 3:
		printer.setForeground( printer.RED )
		printer.out( 'To use this tool you need to pass in at a minimum three arguments: inputfile, outputfile, and JSON path' )
	elif len( args ) == 3:
		file = args[ 0 ]
		outFile = args[ 1 ]
		jsonPath = args[ 2 ]

		f = open( file, 'r+' )
		jsonData = f.read()

		# parse out the json data
		data = json.loads( jsonData )

		files = getDataForJSONPath( data, jsonPath )


		# if we are told to parse we should go through the
		# entire json file and look for "img" items
		if options.parse:
			allImgFromJSON = []

			urlTags = options.urlTags.rsplit( ',' )

			lookForImg( data, allImgFromJSON, urlTags )

			for nFile in allImgFromJSON:
				found = False

				for url in files[ 'regular' ]:
					if nFile[ 'url' ] == url[ 'url' ]:
						found = True
						break

				# since this file was not found we'll attempt to add it to the list
				if found == False:
					if options.interactiveParse == None:
						files[ 'regular' ].append( nFile )
					else:
						printer.setForeground( printer.YELLOW )
						yellow = printer.getEscape()
						printer.setForeground( printer.CYAN )
						printer.doBold = True
						cyan = printer.getEscape()
						yesNo = raw_input( 'Do you want to add the file ' + cyan + '\'' + nFile[ 'url' ] + '\'' + printer.getReset() + ' to preload json ' + yellow + '(y/n): ' )
						sys.stdout.write( printer.getReset() )

						if yesNo == 'y' or yesNo == 'yes':
							files[ 'regular' ].append( nFile )
				


		# now figure out and add the percentages
		totalBytes = 0
		totalBytesRetina = 0
		retinasFound = False

		# we need to duplicate the list of files so if we remove an item we can continue iterating
		filesToCheckOver = files[ 'regular' ][:]
		files[ 'retina' ] = []

		for cFile in filesToCheckOver:
			regularExist = False
			cURL = cFile[ 'url' ]
			rURL = '@2x.'.join( cFile[ 'url' ].rsplit( '.', 1) )

			print rURL

			if os.path.exists( options.cwd + cURL ):
				regularExist = True
				cFile[ 'bytes' ] = os.path.getsize( options.cwd + cURL )
				totalBytes += cFile[ 'bytes' ]
			else:
				printer.setForeground( printer.RED )
				printer.out( 'THE FILE ' + cFile[ 'url' ] + ' DIDN\'T EXIST NOT ADDED TO PRELOAD JSON' )
				files[ 'regular' ].remove( cFile )

			# check if retina images exist
			# this will obviously check for @2x for even audio and video
			# but if the file doesnt exist then it wont be added and if regular does exist that
			# will be added
			if os.path.exists( options.cwd + rURL ):
				retinasFound = True
				retinaBytes = os.path.getsize( options.cwd + rURL )
				files[ 'retina' ].append( { 'url': rURL, 'bytes': retinaBytes, 'type': cFile[ 'type' ] })
				totalBytesRetina += retinaBytes
			elif regularExist:
				files[ 'retina' ].append( { 'url': cFile[ 'url' ], 'bytes': cFile[ 'bytes' ], 'type': cFile[ 'type' ] })
				totalBytesRetina += cFile[ 'bytes' ]




		# print the info header
		printer.setForeground( printer.YELLOW )
		printer.out( '\n\n--- FILE INFO ---' )
		printer.setForeground( printer.CYAN )
		printer.out( 'Total bytes: ' + str( totalBytes ) + '\n' )
		
		# calculate percentages for non-retina load
		for cFile in files[ 'regular' ]:
			cFile[ 'percentage' ] = float( cFile[ 'bytes' ] ) / totalBytes

			# print info about the file
			printer.setForeground( printer.CYAN )
			printer.out( cFile[ 'url' ] + ' -- bytes: ' + str( cFile[ 'bytes' ] ) + ' percentage: ' + str( cFile[ 'percentage' ] ) )

			# remove bytes since we don't want it in the json
			cFile.pop( 'bytes' )


		# calculate percentages for retina load
		printer.out( '\n\nTotal bytes retina: ' + str( totalBytesRetina ) + '\n' )

		for cFile in files[ 'retina' ]:
			cFile[ 'percentage' ] = float( cFile[ 'bytes' ] ) / totalBytes

			# print info about the file
			printer.setForeground( printer.CYAN )
			printer.out( cFile[ 'url' ] + ' -- bytes: ' + str( cFile[ 'bytes' ] ) + ' percentage: ' + str( cFile[ 'percentage' ] ) )

			# remove bytes since we don't want it in the json
			cFile.pop( 'bytes' )






		# time to do some output
		# get the json output
		if options.pretty:
			jsonOutput = json.dumps( data, indent=4, separators=(',', ': ') )
		else:
			jsonOutput = json.dumps( data )
			
		# write out the file	
		f = open( outFile, 'w' )
		f.write( jsonOutput )
		f.close()
	else:
		printer.setForeground( printer.RED )
		printer.out( 'In order to run this script you must provide a JSON file that we will use' )

except(SystemExit, TypeError):
	printer.outReset()

except:
	print "Unexpected error:", sys.exc_info()[0]
	print "AT LINE:" + str( sys.exc_traceback.tb_lineno )

	# if this program crashed or was killed we want to reset the colours quickly
	printer.outReset()

print '\n\n'
