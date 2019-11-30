"""
Code to convert raw draw database into a land draw database.

Needs to have the land mapping database set up (land_mapping.txt). This is created by running
search_UTC_logs_for_card_definitions.py.



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
    already_processed = set()
    cnt = 0
    for row in f_in:
        data = row.split(';')
        transact = data[0]
        # Eat redundant rows.
        if transact in already_processed:
            continue
        already_processed.add(transact)
        delim = str(utils.draw_database_separator)
        for pos in range(utils.draw_database_header_size,len(data)):
            if not data[pos] == delim:
                data[pos] = land_mapper.get(int(data[pos].strip()), '?')
        out_row = ';'.join(data) + '\n'
        f_out.write(out_row)
        if f_prod is not None:
            f_prod.write(out_row)

