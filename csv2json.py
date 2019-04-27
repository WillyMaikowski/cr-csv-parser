#!/usr/bin/env python

import csv
import json
import os
import sys
import io
import re

cast = { 'string': str, 'int': int, 'boolean': ( lambda x: x == 'true' ) }

def camel2snake( s ):
    if isinstance( s, list ): return [ camel2snake( sub ) for sub in s ]
    s1 = re.sub( '(.)([A-Z][a-z]+)', r'\1_\2', s )
    return re.sub( '([a-z0-9])([A-Z])', r'\1_\2', s1 ).lower()

def csv2json( filepath ):
    f = io.open( filepath, 'r', encoding='utf-8' )
    rows = csv.reader( f )
    #print( filepath )

    line = 0
    data = []
    for r in rows:
        line += 1

        if line == 1:
            cols = camel2snake( r )
            continue

        if line == 2:
            types = [ el.lower() for el in r ]
            continue

        if len( cols ) != len( r ):
            print( 'Bad line in file ', filepath, '. Ignored line:', line )
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
    if len( data ) <= 0: return

    filepath = filepath.split( '/' )
    if len( filepath ) > 1: filepath.pop( 0 )

    newpath = os.path.join( 'json/', '/'.join( filepath ) )
    newpath = os.path.splitext( newpath )[0]+'.json'
    os.makedirs( os.path.dirname( newpath ), exist_ok=True )
    f = open( newpath, 'w' )
    f.write( json.dumps( data, sort_keys=True, indent=4 ) )
    f.close()



if __name__ == '__main__':

    indir = sys.argv[1]
    if not indir:
        print( 'You must add a filename or directory' )
        quit()


    if os.path.isfile( indir ):
        if os.path.splitext( indir )[1] != '.csv':
            print( 'The file have to be csv' )
        else:
            csv2json( indir )
        quit()

    for path, _, filenames in os.walk( indir ):
        for filename in filenames:
            if os.path.splitext( filename )[1] != '.csv': continue
            csv2json( os.path.join( path, filename ) )
