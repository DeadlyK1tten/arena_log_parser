"""

Parse the UTC logs files in the 'UTC_logs' sub-directory.


"""

import glob
import os
import traceback

import parsercode.utils as utils
import parsercode.parsefile as parsefile


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        utils.SetWorkingDirectory(__file__)
        utils.Log('Clearing the last draw database')
        f = open('draw_database_last.txt', 'w')
        file_list = glob.glob(os.path.join('UTC_logs', 'UTC_log*.log'))
        for filename in file_list:
            parsefile.ProcessFile(filename, verbose=False, append_production=True)
            utils.ArchiveUTClog(filename)
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
