"""
Create the summary data file, which aggregates draw data.


"""


import traceback

import parsercode.utils as utils
import parsercode.aggregator as aggregator


def main():
    utils.SetWorkingDirectory(__file__)
    aggregator.main()

if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        main()
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
