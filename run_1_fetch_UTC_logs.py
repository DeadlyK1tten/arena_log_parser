"""
Attempt to copy log files of form "UTC_Log <date> <time>.log"

Thanks to user Ragnoraok for pointing out the location of these files; much more convenient.

On my machine, they are created by Arena in C:\\Program Files (x86)\\Wizards of the Coast\\MTGA\\MTGA_Data\\Logs\\Logs

They are copied to the UTC_logs subdirectory.

Note: If the path does not work on your machine, you will need to change the code to point to the correct
directory. If you do that, rename your version so it does not crash into any updated versions of this file.


"""

import glob
import os
import traceback
import shutil

import parsercode.utils as utils

# Change the directory below if needed...
source_dir = 'C:\\Program Files (x86)\\Wizards of the Coast\\MTGA\\MTGA_Data\\Logs\\Logs'

def main():
    utils.Log('Looking for logs in {0}\n'.format(source_dir))
    utils.SetWorkingDirectory(__file__)
    try:
        file_list = glob.glob(os.path.join(source_dir, 'UTC_log*.log'))
    except:
        utils.Log('Cannot get list of files at: {0}\n'.format(source_dir))
        raise
    existing_file_list_1 = glob.glob(os.path.join('UTC_logs', 'UTC_log*.log'))
    existing_file_list_2 = glob.glob(os.path.join('UTC_logs', 'parsed', 'UTC_log*.log'))
    existing = existing_file_list_1 + existing_file_list_2
    existing = [os.path.basename(x) for x in existing]
    for filename in file_list:
        basename = os.path.basename(filename)
        if basename in existing:
            utils.Log('Already in UTC_Logs, or parsed: {0}\n'.format(basename))
        else:
            utils.Log('Attempting copy: {0}\n'.format(filename))
            shutil.copyfile(filename, os.path.join('UTC_logs', basename))


if __name__ == '__main__':
    try:
        utils.Log('Trying to copy log (new) log files.\n')
        main()
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
