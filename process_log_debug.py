"""
Debugging version. Doesn't write to draws.txt, but draws_debug.txt
"""


import parsercode.utils as utils


if __name__ == '__main__':
    utils.Log('Starting\n')
    try:
        f = open('draws_debug.txt', 'w')
        f.close()
        utils.ProcessFile('output_log.txt', debug=True)
    except Exception as ex:
        utils.Log(str(ex))
        raise
