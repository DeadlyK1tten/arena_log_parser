"""
deck_manager: a utility to manage Arena decks.
Choose whether to take exported deck (on clipboard) and save to file,
or to copy a file to the clipboard.

Decks have a date associated with them, so easy to save an evolving deck.

Need to install pyperclip.
Google: "pip install pyperclip"

"""

import pyperclip
import os
import datetime
import glob


class FinishedEvent(Exception):
    pass


def import_deck():
    s = pyperclip.paste()
    s = s.replace('\r', '')
    print('Deck:')
    print(s)
    name = input('Name to use? (Empty to not save) > ')
    name = name.strip()
    if len(name) == '':
        print('Abort!')
        return
    ddate = datetime.date.today().isoformat()
    ddate = ddate.replace('-', '_')
    full_name = os.path.join('decks', f'{ddate}_{name}.txt')
    f = open(full_name, 'w')
    f.write(s)
    f.close()

def load_deck():
    flist = glob.glob('decks\\*.txt')
    for pos in range(0, len(flist)):
        full_name = flist[pos]
        ddir, fname = os.path.split(full_name)
        if fname.lower() == 'readme.txt':
            continue
        shortname = fname[11:]
        print(f'{pos}\t{shortname}\t{full_name}')
    opt = input('Choice >')
    try:
        opt = int(opt.strip())
    except:
        return
    targ = flist[pos]
    print(f'Copying {targ} to clipboard')
    f = open(targ, 'r')
    deck = ''
    for row in f:
        row = row.strip()
        if len(row) == 0:
            continue
        deck += (row + '\r\n')
    print(deck)
    pyperclip.copy(deck)

def do_loop():
    print('Options: (s)ave deck from clipboard, (l)oad deck to clipboard, (q)uit.')
    opt = input('Choice >')
    opt = opt.lower()
    if opt == 'q':
        raise FinishedEvent('Done')
    if opt == 's':
        import_deck()
    if opt == 'l':
        load_deck()
    do_loop()



def main():
    print('Starting')
    try:
        do_loop()
    except FinishedEvent:
        pass


if __name__ == '__main__':
    main()