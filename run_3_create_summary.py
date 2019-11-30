"""
Create the summary data file, which aggregates draw data.


"""


import traceback

import parsercode.utils as utils
import parsercode.aggregator as aggregator


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        utils.SetWorkingDirectory(__file__)
        aggregator.main()
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
