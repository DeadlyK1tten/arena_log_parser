"""
Debugging version of draw database


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
        parsefile.ProcessFile('output_log.txt', verbose=True, append_production=False)
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
