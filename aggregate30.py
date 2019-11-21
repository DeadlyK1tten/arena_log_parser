"""
Run this script which blasts through the draws.txt to create a "summary30.txt"

Need to run "process_log.py" first.

Only looks for the 30 land test (code "30")

Main trick: need to ignore duplicated transactions.



"""

import code.utils

def main():
    print('Starting the 30-land aggregation')
    code.utils.aggregate30()


if __name__ == '__main__':
    main()
