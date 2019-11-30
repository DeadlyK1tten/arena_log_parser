"""
Code to convert raw draw database into a land draw database.

"""

from parsercode.utils import Log
import parsercode.utils as utils

def build_land_draw_database(use_last=False):
    Log('Starting land draw database construction')
    if use_last:
        f_in = open('draw_database_last.txt', 'r')
    f_out = open('land_draws_last.txt', 'w')
    if use_last:
        f_prod = None
    else:
        f_prod = open('land_draws.txt', 'a')
    land_mapper = utils.LoadLandMapping()
    cnt = 0
    for row in f_in:
        data = row.split(';')
        for pos in range(8,len(data)):
            if not data[pos] == '-1':
                data[pos] = land_mapper.get(int(data[pos].strip()), '?')
        out_row = ';'.join(data) + '\n'
        f_out.write(out_row)

