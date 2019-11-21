"""
Process log file.

(0) Install a recent version (version 3+) of Python. Learn how to run scripts.
(1) Copy output_log.txt to this directory.
(2) Run this script.
(3) Creates/updates files: log.txt (log file), draws.txt (database of parsed draws).

NOTE: Eventually will archive the log files. Right now, you have to do that manually. You need to replace output_log.txt
each time you run.

NOTE: Mulligans are not being tracked due to a design change. Will need to fix "soon"

No idea whether Bo3 will work.

TODO: Redesign to track mulligans. (Currently, resets deck status after initial draw, but we need to keep looking.
"""


import code.utils as utils


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        utils.ProcessFile('output_log.txt')
    except Exception as ex:
        utils.Log(str(ex))
        raise
