"""
Process log file.

(0) Install a recent version (version 3+) of Python. Learn how to run scripts.
(1) Copy output_log.txt to this directory.
(2) Run this script.
(3) Creates/updates files: log.txt (log file), draws.txt (database of parsed draws).

NOTE: Eventually will archive the log files. Right now, you have to do that manually. You need to replace output_log.txt
each time you run.

NOTE: Mulligan tracking fixed.

No idea whether Bo3 will work.

"""

import os
import sys
import traceback

import parsercode.utils as utils


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        if not os.path.exists('output_log.txt'):
            utils.Log('Arena log file "output_log.txt" not in running directory (normally same as process_log.py')
            utils.Log('Current working directory = {0}\n'.format(os.getcwd()))
            o = input('Hit return to continue >')
        else:
            utils.ProcessFile('output_log.txt')
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        traceback.print_exc(file=sys.stdout)
        o = input('Hit return to continue >')
        raise
