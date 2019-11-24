"""
Run this script which blasts through the draws.txt to create a "summary.txt"

Need to run "process_log.py" first.

Processes both singleton and "30" trials.

Main trick: need to ignore duplicated transactions.

Not heavily tested... "aggregate30.py" was tested more.
"""

import code.utils

def main():
    print('Starting aggregation')
    code.utils.aggregate()


if __name__ == '__main__':
    main()
