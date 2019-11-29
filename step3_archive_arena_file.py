"""
archive output_log.txt to archive

Tested on Windows, will it work anywhere else>
"""

import glob

import os


def main():
    print('starting')
    if not os.path.exists('output_log.txt'):
        print('no log file')
        return
    file_list = glob.glob(os.path.join('archive', 'output_log*.txt'))
    for n in range(0, len(file_list)+1):
        attempt = os.path.join('archive', 'output_log_{0:03}.txt'.format(n))
        if not os.path.exists(attempt):
            os.rename('output_log.txt', attempt)
            break

if __name__ == '__main__':
    main()