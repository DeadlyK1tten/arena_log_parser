"""
Create a land draw database from "draw_database.txt"

Need to get land mappings updated (run_search_UTC_logs_for_card_definitions.py)


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
        land_mapper.build_land_draw_database(use_last=False)
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
