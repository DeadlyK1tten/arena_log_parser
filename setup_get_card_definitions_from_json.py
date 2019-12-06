"""
Get land/non-land definitions from "database.json", which is part of the open source MTGA Tool.



"""

import json


import glob
import os
import traceback
import pprint

import parsercode.utils as utils
import parsercode.parsefile as parsefile


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        utils.SetWorkingDirectory(__file__)
        land_mapping = utils.LoadLandMapping()
        utils.Log('Initial entries: {0}\n'.format(len(land_mapping)))
        try:
            f_in = open('database.json', 'r')
        except:
            input('Need to get database.json from MTGA Tool repository. Hit return to quit >')
            raise
        info = json.load(f_in)
        cardz = info['cards']
        for k in cardz:
            num_id = cardz[k]['id']
            ttype = cardz[k]['type']
            is_land = 'land' in ttype.lower()
            if is_land:
                land_code = 'L'
            else:
                land_code = 'N'
            # Do a sanity check
            if num_id in land_mapping:
                if not land_mapping[num_id] == land_code:
                    raise ValueError('Inconsistent Data!')
            land_mapping[num_id] = land_code
        s = pprint.pformat(land_mapping)
        f = open('land_mapping.txt', 'w')
        f.write(s)
        f.close()
        print(s)
        print('number of entries:', len(land_mapping))

    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
