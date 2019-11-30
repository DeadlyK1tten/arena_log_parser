"""
Debugging version of tool to convert draw database to land draw database


"""

import glob
import os
import traceback

import parsercode.utils as utils
import parsercode.land_mapper as land_mapper


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        utils.SetWorkingDirectory(__file__)
        land_mapper.build_land_draw_database(use_last=True)
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
