# arena_log_parser
MTG Arena Log Parser

Use at own risk; no warranty of any kind provided.

Since all the code does is read some text files and writes other ones, you really would need to
take a lot of effort to break things.

Testing section down below gives a summary of what to do.

**See the file RunningThePackage.md for help.**

Note that there was a GitHub package that forked from the MTGA Tool to generate a big study.
However, one would need to get the code up-to-date with respect to MTGA Tool, and get 
cooperation with those developers. Obviously, a much larger project. Any ongoing statistical
analysis would have to supported by the tracker developers, and would obviously be more
powerful.
https://github.com/dougmill/MTG-Arena-Tool/tree/shuffler-stats

Note: includes a basic Arena deck manager script (deck_manager.py). This script requires 
installation of a package that is not in base Python. Google "python pip install instructions"

*NOTE: Land Draw testing added; not heavily documented yet.*

Note: Some new cards were added to Arena, and the definitions are missing for the land draw
analysis.

# Testing

The first test run was the "30 land test", described below.

The next test will be a deck position test. This test will use all decks with 40, 59. 60 card
libraries (59=Brawl). This test will not require any special behaviour - other than using minimal
deck sizes.


## "30" Test - 30 Lands, Look for Bias

(1) Create the following deck list.

Deck
30 Plains (ELD) 250
30 Swamp (ELD) 258

(2) Play against Sparky, maybe mulligan, then concede.

(3) Repeat (2)...

*Follow the instructions in RunningThePackage.md*

What the test does.

The script looks for a deck, defined by the numeric card codes, with 70397 the Plains, 70405 the Swamp.
The following line has to appear *exsctly*

 "deckMessage": { "deckCards": [ 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70397, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405, 70405 ]


The final step is to create a summary that looks like

30,Amaz1ngK1tten,0,0,0,0,0,1,0,0=1

This is a summary of the trials.

30 = "deck code" (test to be run; the 30 Plains/Swamp test. We could create multiple tests that can coexist in archives.)
Amaz1ngK1tten = user name.
0,0,0,0,0,1,0,0 = summary of the Swamp counts for all the possible number of initial swamps, from 0 to 7. In this case,
it was one trial, with 5 swamps in the initial hand.
"=1" = trial count (1).

There is also a "30MULL" test that includes mulligans. It is very easy to generate a lot 
of mulligans, but the mulligan version is not expected to show a bias (based on Douglas' earlier
work). 

### Why this Deck?

By being 100% lands, the Best-of-One hand picker is nullified. It has no choice but to pick one at random. This means
we do not need to go into Bo3.

By looking at the relative # of swamps and plains drawn, a systematic deviation of draw probabilities based on the
initial position of cards should show up. We use a 30/30 on the basis that we cannot be sure whether the bias is towards
the front or back. We could go for a 50/10 split to isolate the front/back later.

Although it is easy to generate a lot of shuffles with mulligans, the argument is that the mulligan reuses the shuffled
deck, and so any bias is obliterated. Mulligans are stored, but flagged as such, allowing for later analysis of draws
that might want to use mulligans.

## Deck Position Test

This test has not yet been implemented. It will look at all initial draws for decks with
initial library sizes of 40, 59, and 60 (as three separate tests).

It will attempt to see whether cards at the front (or back) of the initial library are 
favoured.

This test runs into the Bo1 initial draw mangler. The hope is that the bias created by the
hand picker (which is based solely on land/nonland status) is smaller than the bias we are 
testing for.

An initial version based on singleton decks was built, but the singleton requirement is being
dropped (as per the suggestion by Sirius).

# Custom Tests

The file "custom_tests.py" (found under parsercode) explains how to add your own tests.
The "30 land test" is implemented in there. If you want to do an exact analogue to that 
test, how to do so is explained.

You might need to know a bit more about Python if you to change the test logic. However, 
doing so should be easier, since you just need to worry about the logic of the actual test
analysis, and everything else is handled for you.