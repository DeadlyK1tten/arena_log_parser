"""
Process all logs in archive

Only need to use this if rebuilding draws.txt

Writes to draws_debug.txt

"""

import glob
import os

import code.utils as utils


if __name__ == '__main__':
    utils.Log('Starting\n')
    # Clear the debug file.
    f = open('draws_debug.txt', 'w')
    f.close()
    file_list = glob.glob(os.path.join('archive', 'output_log*.txt'))
    for filename in file_list:
        try:
            utils.ProcessFile(filename, debug=True)
        except Exception as ex:
            utils.Log(str(ex))
            raise
