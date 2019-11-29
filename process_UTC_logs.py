"""
Process the log files of the format "UTC_Log <date> <time>.log"

Thanks to user Ragnoraok for pointing out the location of these files; much more convenient.

On my machine, they are created by Arena in C:\\Program Files (x86)\\Wizards of the Coast\\MTGA\\MTGA_Data\\Logs\\Logs

They then need to be copied to the UTC_logs subdirectory. (Below where this file sits.)

All log files are parsed, and initial draw information appended to draws.txt

Once processed, the files are moved to the "parsed" subdirectory of "UTC_logs"
(That is "<code base>\\UTC_logs\\parsed")

To re-run the parsing, move the files from "parsed" to "UTC_logs". Since data are appended to draws.txt,
you probably need to delete the existing file (or at least the appropriate data).

(Note that if the same log file is processed more than once, "draws.txt" will get repeated rows. This will be
picked up during the aggregation; each row has a transaction ID, and repeats are detected and ignored.

"""

import glob
import os
import traceback

import parsercode.utils as utils


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        utils.SetWorkingDirectory(__file__)
        file_list = glob.glob(os.path.join('UTC_logs', 'UTC_log*.log'))
        for filename in file_list:
            utils.ProcessFile(filename, debug=False, verbose=False)
            utils.ArchiveUTClog(filename)
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
