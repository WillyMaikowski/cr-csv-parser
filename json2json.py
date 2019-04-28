#!/usr/bin/env python

import json
import os

config = {
    'alliance_badges': {
        '_s': 'json/assets/csv_logic/alliance_badges.json',
        'id': ( lambda i, x: 16000000+i )
    },
    'arenas': {
        '_s': 'json/assets/csv_logic/arenas.json',
        '_filter': ( lambda x: x['is_in_use'] == True ),
        '_tid': [ 'tid|title', 'subtitle_tid|subtitile' ],
        'key': ( lambda i, x: "league{}".format( x['league'] ) if 'league' in x else "arena{}".format( x['arena'] ) ),
        'arena_id': ( lambda i, x: x['arena']-x['league'] if 'league' in x else x['arena'] ),
        'id': ( lambda i, x: 54000000+x['arena'] )
    }#,
    #'cards': {},
    #'cards_stats': {},
    #'challenges': {},
    #'chest_order': {},
    #'clan_chest': {},
    #'game_modes': {},
    #'rarities': {},
    #'regions': {},
    #'tournaments': {},
    #'treasure_chests': {}
}

for out in config:
    f = open( config[out]['_s'], 'r', encoding='utf-8' )
    data = json.load( f )
    f.close()

    if '_filter' in config[out]:
        data = list( filter( config[out]['_filter'], data ) )

    for i, d in enumerate( data ):
        for key in config[out]:
            if key[0] == '_': continue
            d[key] = config[out][key]( i, d )

        data[i] = d

    os.makedirs( 'out/', exist_ok=True )
    f = open( os.path.join( 'out/', out+str( '.json' ) ), 'w' )
    f.write( json.dumps( data, indent=4 ) )
    f.close()
