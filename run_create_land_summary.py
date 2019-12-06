"""
Create the land draw summary table


"""


import traceback

import parsercode.utils as utils
import parsercode.aggregator as aggregator


def main():
    utils.SetWorkingDirectory(__file__)
    aggregator.run_land_counts()

if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        main()
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
