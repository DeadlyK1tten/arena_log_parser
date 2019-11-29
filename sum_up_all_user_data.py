"""
Script to generate mega-summary


"""


import glob
import os
import traceback

import parsercode.utils as utils


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        utils.SetWorkingDirectory(__file__)
        utils.SumUpAllUserData('all_user_aggregates.txt')
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
