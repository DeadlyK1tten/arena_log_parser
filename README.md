# arena_log_parser
MTG Arena Log Parser

Python MTG Arena log parser.

Use at own risk; no warranty of any kind provided.

Since all the code does is read some text files and writes other ones, you really would need to
take a lot of effort to break things.

Testing section down below gives a summary of what to do.

See the file RunningThePackage.md for help.

Note that there was a GitHub package that forked from the MTGA Tool to generate a big study.
However, one would need to get the code up-to-date with respect to MTGA Tool, and get 
cooperation with those developers. Obviously, a much larger project. Any ongoing statistical
analysis would have to supported by the tracker developers, and would obviously be more
powerful.
https://github.com/dougmill/MTG-Arena-Tool/tree/shuffler-stats

Note: includes a basic Arena deck manager script (deck_manager.py). This script requires 
installation of a package that is not in base Python. Google "python pip install instructions"

# What's Changed

Made some changes that appear to have fixed issues. What was happening was that I needed
to take into account player ID changing; for bot matches, always player ID of 1. Still need to look
at it.

- Mulligan tracking fixed.
- Archive script.
- Brawl, singleton.
- Aggregation script.

# Upcoming Work

Immediate needs:

- Create a script that works from the "UTC" logs found in the executable directory.
- Aggregation fixes.
- Multi-User Aggregation.
- User Docs (assuming stability)

After that, there will be a redesign: the log parser will first generate an initial draw 
database, *of all draws*. Then, the aggregation scripts will blast through the master draw file,
and then extract the test aggregate data.

Why make this change? People can use whatever tools they want to analyse the draw database. For 
example, masochists could do analysis in Excel (not recommended). Also, the only code that is 
vulnerable to WotC changing the log file structure is the parsing code. By isolating it to a 
self-contained package, it can be replaced by whatever else people can come up with.

Other stuff:

- Bo3 mode testing.
- More information on game: event type, opponent, gameplay time stamp.
- Card database: map the card code to card data, most importantly, land/nonland status.
- Automation. (Current project does not touch anything outside local directories.)
- For somebody else: can data be aggregated automatically on some central point?

# Testing

How the testing works.

## "30" Test - 30 Lands, Look for Bias

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

### Why this Deck?

By being 100% lands, the Best-of-One hand picker is nullified. It has no choice but to pick one at random. This means
we do not need to go into Bo3.

By looking at the relative # of swamps and plains drawn, a systematic deviation of draw probabilities based on the
initial position of cards should show up. We use a 30/30 on the basis that we cannot be sure whether the bias is towards
the front or back. We could go for a 50/10 split to isolate the front/back later.

Although it is easy to generate a lot of shuffles with mulligans, the argument is that the mulligan reuses the shuffled
deck, and so any bias is obliterated. Mulligans are stored, but flagged as such, allowing for later analysis of draws
that might want to use mulligans.

## Brawl/Singleton

If you run a deck with no repeated cards, will be detected as Brawl (59 cards in library) or 
singleton. Singleton 60 looks like the most interesting possibility, and has trial code
 "SING60".

In order to meet the no repeated card rule, cannot have the same version of a basic land. 

Since no cards are repeated, we can determine the exact initial position of each card in the 
initial draw. We can then count the number of times we see each card at each position.

If your deck is not picked up, you will need to look at the log to see what repeated cards
exist.

The known issue with this test is that the Bo1 initial draw mangler will affect the probability
distribution of land/non-land cards (somehow). Since the algorithm just eliminates extremes 
from both ends, the land/non-land probability will have a smaller effect. Testers could attempt
to cancel this out by having some decks with the lands at the front, and not the back of the
deck list.