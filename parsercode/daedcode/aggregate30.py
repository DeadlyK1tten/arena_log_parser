"""
Run this script which blasts through the draws.txt to create a "summary30.txt"

Need to run "process_log.py" first.

Only looks for the 30 land test (code "30")

Main trick: need to ignore duplicated transactions.


How the testing works.

(1) Create the following deck list.

Deck
30 Plains (ELD) 250
30 Swamp (ELD) 258

(2) Play against Sparky, maybe mulligan, then concede.

(3) Repeat (2)...

(4) Once done, copy the log file output_log.txt to this directory.

The script looks for a deck, defined by the numeric card codes, with 70397 the Plains, 70405 the Swamp.
The following line has to appear *exsctly*

 "deckMessage": { "deckCards": [ 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405 ]

(5) Run process_log.py to take data out of the log file, and puts the draw information into a text file "draws.txt"

(6) This can be done multiple times, new runs are added to the data set. If you run the same file multiple times,
the same draw will appear multiple times. This is not a problem; repeat copies of the same draw are ignored in aggregation.

(7) Run this script to generate the summary file summary_30.txt

This gives a summary, as follows:

30,Amaz1ngK1tten,0,0,0,0,0,1,0,0

This is a summary of the trials.

30 = "deck code" (test to be run; the 30 Plains/Swamp test. We could create multiple tests that can coexist in archives.)
Amaz1ngK1tten = user name.
0,0,0,0,0,1,0,0 = summary of the Swamp counts for all the possible number of initial swamps, from 0 to 7. In this case,
it was one trial, with 5 swamps in the initial hand.

Why this Deck?
===============

By being 100% lands, the Best-of-One hand picker is nullified. It has no choice but to pick one at random. This means
we do not need to go into Bo3.

By looking at the relative # of swamps and plains drawn, a systematic deviation of draw probabilities based on the
initial position of cards should show up. We use a 30/30 on the basis that we cannot be sure whether the bias is towards
the front or back. We could go for a 50/10 split to isolate the front/back later.

Although it is easy to generate a lot of shuffles with mulligans, the argument is that the mulligan reuses the shuffled
deck, and so any bias is obliterated. Mulligans are stored, but flagged as such, allowing for later analysis of draws
that might want to use mulligans.
"""

import parsercode.utils

def main():
    print('Starting the 30-land aggregation')
    parsercode.utils.aggregate30()


if __name__ == '__main__':
    main()
