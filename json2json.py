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
    },
    #'cards': {},
    #'cards_stats': {},
    'challenges': {
        '_s': 'json/assets/csv_logic/survival_modes.json',
        '_filter': ( lambda x: x['enabled'] and 'name' in x ),
        'key': ( lambda i, x: x['name'] ),
        'id': ( lambda i, x: 65000000+i )
    },
    'chest_order': {
        '_s': 'json/assets/csv_logic/chest_order.json'
    },
    'clan_chest': {
        '_s': 'json/assets/csv_logic/globals.json',
        '_global': {
            '1v1': ( lambda x: { el['name'].split( '_' )[-1].lower(): list( el['number_array'].values() ) for el in x if 'CLAN_CROWN_CHEST_' in el['name'] and 'number_array' in el  } ),
            '2v2': ( lambda x: { el['name'].split( '_' )[-1].lower(): list( el['number_array'].values() ) for el in x if 'CLAN_TEAM_VS_TEAM_CHEST_' in el['name'] and 'number_array' in el  } )
        }
    },
    'game_modes': {
        '_s': 'json/assets/csv_logic/game_modes.json',
        '_tid': [ 'tid|title', 'clan_war_description|clan_war_description' ],
        'id': ( lambda i, x: 72000000+i )
    },
    'rarities': {
        '_s': 'json/assets/csv_logic/rarities.json'
    },
    'regions': {
        '_s': 'json/assets/csv_logic/regions.json',
        'id': ( lambda i, x: 57000000+i ),
        'key': ( lambda i, x: x['name'] ),
        'name': ( lambda i, x: x['display_name'] )
    },
    'tournaments': {
        '_s': 'json/assets/csv_logic/tournament_tiers.json',
        '_filter': ( lambda x: 'disabled' not in x or not x['disabled'] ),
        'key': ( lambda i, x: x['name'] )#,
        #'prizes': ( lambda i, x: [] )
    }#,
    #'treasure_chests': {
    #    '_s': 'json/assets/csv_logic/treasure_chests.json',
    #}
}

for out in config:
    f = open( config[out]['_s'], 'r', encoding='utf-8' )
    data = json.load( f )
    f.close()

    if '_filter' in config[out]:
        data = list( filter( config[out]['_filter'], data ) )

    if '_global' in config[out]:
        new_data = {}
        for key in config[out]['_global']:
            new_data[key] = config[out]['_global'][key]( data )
        data = new_data

    if isinstance( data, list ):
        for i, d in enumerate( data ):
            for key in config[out]:
                if key[0] == '_': continue
                d[key] = config[out][key]( i, d )

        data[i] = d

    os.makedirs( 'out/', exist_ok=True )
    f = open( os.path.join( 'out/', out+str( '.json' ) ), 'w' )
    f.write( json.dumps( data, indent=4 ) )
    f.close()
