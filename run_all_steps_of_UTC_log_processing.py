"""

Do all the processing steps of UTC Log processing. Just need to run this one script. However, if one is not
sure what is happening, running one step at a time will be clearer.

- Fetches the logs.
- Adds to the draw database.
- Creates the summary file ("summary.txt")

"""


import traceback

import parsercode.utils as utils
import run_1_fetch_UTC_logs
import run_2_parse_UTC_logs
import run_3_create_summary


def main():
    utils.SetWorkingDirectory(__file__)
    run_1_fetch_UTC_logs.main()
    run_2_parse_UTC_logs.main()
    run_2_parse_UTC_logs.main()


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        main()
    except Exception as ex:
        utils.Log(traceback.format_exc() + '\n')
        raise
