"""
Process the log files of the format "UTC_Log <date> <time>.log"
Debug version: all output is written to "draws_debug.txt" (which is overwritten). Use "process_UTC_logs.py" to
write data to "draws.txt."

On my machine, they are created by Arena in C:\\Program Files (x86)\\Wizards of the Coast\\MTGA\\MTGA_Data\\Logs\\Logs

They then need to be copied to the UTC_logs subdirectory. (Below where this file sits.)

All log files are parsed, and initial draw information appended to draws.txt

Once processed, the files are moved to the "parsed" subdirectory of "UTC_logs"
(That is "<code base>\\UTC_logs\\parsed")

To re-run the parsing, move the files from "parsed" to "UTC_logs". Since data are appended to draws.txt,
you probably need to delete the existing file (or at least the appropriate data).


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
        f.close()
        file_list = glob.glob(os.path.join('UTC_logs', 'UTC_log*.log'))
        for filename in file_list:
            parsefile.ProcessFile(filename, append_production=False, verbose=False)
            utils.ArchiveUTClog(filename)
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
