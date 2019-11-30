"""
Generate the land mapping database ("land_mapping.txt") by scanning all UTC logs (including previously
parsed files).

The land database maps known cards to land/non-land status. The file is a text representation of a Python
dictionary. For example:

{7347: 'L',
 19577: 'N',
 32675: 'N',
 ...}

The numeric codes are the card ID's, the 'L' and 'N' represent 'land'/'nonland.'

Unless we raid the card database from a tracker (as suggested by Sirius), we can only map the cards that are seen in
play. This will include anything in an initial draw, but we can miss cards in the library.

The file "land_mapping_repository.txt" is a copy of DK's land mapping. However, it is totally non-comprehensive.
However, if a player has a decent database of recorded game logs, pretty much all constructed cards used by the player
will be mapped. The only cards likely to be missed are cards played in draft which are rarely used and managed not be
drawn in any run.

"""

import glob
import os
import traceback
import pprint
import ast

import parsercode.utils as utils
import parsercode.parsefile as parsefile


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        utils.SetWorkingDirectory(__file__)
        land_mapping = utils.LoadLandMapping()
        print('Initial entries:', len(land_mapping))
        # Process both the UTC_Logs and the "parsed" directories. Need everything.
        file_list = glob.glob(os.path.join('UTC_logs', 'parsed', 'UTC_log*.log'))
        for filename in file_list:
            parsefile.GetCardDefinitions(filename, land_mapping)
        file_list = glob.glob(os.path.join('UTC_logs', 'UTC_log*.log'))
        for filename in file_list:
            parsefile.GetCardDefinitions(filename, land_mapping)
        s = pprint.pformat(land_mapping)
        f = open('land_mapping.txt', 'w')
        f.write(s)
        f.close()
        print(s)
        print('number of entries:', len(land_mapping))

    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
