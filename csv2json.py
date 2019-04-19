#!/usr/bin/env python

import csv
import json
import os
import sys

cast = { 'string': str, 'int': int, 'boolean': ( lambda x: x == 'true' ) }

def csv2json( filepath ):
	f = open( filepath )
	rows = csv.reader( f )

	line = 0
	data = []
	for r in rows:
		line += 1

		if line == 1:
			cols = r
			continue

		if line == 2:
			types = [ el.lower() for el in r ]
			continue

		d = {}
		if r[0] == '': d = data.pop()
		for i in range( len( cols ) ):
			if r[i] == '': continue

			key = cols[i]
			value = cast[ types[i] ]( r[i] )

			if key not in d:
				d[key] = value
			elif isinstance( d[key], list ):
				d[key].append( value )
			else:
				d[key] = [ d[key], value ]

		data.append( d  )

	f.close()

	filepath = filepath.split( '/' )
	if len( filepath ) > 1: filepath.pop( 0 )

	newpath = os.path.join( 'json/', ''.join( filepath ) )
	newpath = os.path.splitext( newpath )[0]+'.json'
	os.makedirs( os.path.dirname( newpath ), exist_ok=True )
	f = open( newpath, 'w' )
	f.write( json.dumps( data ) )
	f.close()



if __name__ == '__main__':

	indir = sys.argv[1]
	if not indir:
		print( 'Debe ingresar un directorio o un archivo' )
		quit()

	if os.path.isfile( indir ):
		if os.path.splitext( indir )[1] != '.csv':
			print( 'El archivo debe ser csv' )
		else:
			csv2json( indir )
		quit()

	for path, _, filenames in os.walk( indir ):
		for filename in filenames:
			if os.path.splitext( filename )[1] != '.csv': continue
			csv2json( os.path.join( path, filename ) )

