"""
custom_tests.py

This file gives an example of how to build a test that is looking for specific cards, using the
"30-land" test as an example. If a user wants to build their own custom tests, the easiest place is to start with
the example here.

The 30-land test deck definition itself is found within "decks.py"

The objective is to not touch this file (other than adding more documentation) so it is safe for people to keep
their own copies of the file, and update all of the other code.

To add your own test that works like the 30-land test, do the following.

(1) Add the deck definition to "decks.py", following the pattern for the "30" test. You need a deck list, and
a target card, and a new "test code".

(2) Copy the Test30() class code, changing the name of the class.

(3) In the __init__ function, change the deck code you are looking for to match the one added to decks.py in step (1).

(4) Fix the GetOutput() function to use you deck code.

Note that the "30 land test" has two associated tests, Test30(), and Test30Mulligan(). You will need to think about
how you want to handle mulligans. The ProcessRow() method has code that looks at the mulligan_count.

Note that if you do not want to exactly follow the logic of the "30 land test," you will need to customise the
ProcessRow() code to get the behaviour you want.
"""


import parsercode.decks as decks
from parsercode import utils as utils
from parsercode.utils import Test


class Test30(Test):  # If you want to create your own test, change "class Test30(Test) -> class <MYTESTNAME>(Test):
    """
    30 land test: deck with 30 plains, 30 swamps, count the number of swamps.

    Only looks at initial draw, not mulligans.

    Defeats the B01 hand picker by being 100% lands. There should be no bias between swamps vs. plains.

    As a result, ignores mode.
    """
    def __init__(self, user='?'):
        super().__init__(user)
        self.total = [0] * 8
        # Find the deck in the list found in decks.py
        for deck in decks.target_decks:
            if deck["code"] == '30':
                self.target = deck["target_card"]
                self.Deck = deck['deck']


    def ProcessRow(self, user, draw, deck, mulligan_count, mode):
        """
        As per class description, mode does not matter.
        :param user:
        :param draw:
        :param deck:
        :param mulligan_count:
        :param mode:
        :return:
        """
        if not mulligan_count == 0:
            return
        if utils.decks_equal(deck, self.Deck):
            cnt = sum([x == self.target for x in draw])
            self.User = user
            self.total[cnt] += 1

    def GetOutput(self):
        # If creating your own, change the '30' in the next line to be your test cocde.
        row = ['30', self.User] + [str(x) for x in self.total]
        out = ','.join(row) + '={0}\n'.format(sum(self.total))
        return out


class Test30Mulligan(Test30):
    """
    30 land test, including mulligans.

    Easy to build this up. However, not expected to have a bias based on Douglas' earlier arguments.

    NOTE: This test includes all draws, not only mulligans.

    If you are creating your own custom tests, you will need to decide what you are doing with mulligans.
    """
    def ProcessRow(self, user, draw, deck, mulligan_count, mode):
        if utils.decks_equal(deck, self.Deck):
            cnt = sum([x == self.target for x in draw])
            self.User = user
            self.total[cnt] += 1

    def GetOutput(self):
        row = ['30MULL', self.User] + [str(x) for x in self.total]
        out = ','.join(row) + '={0}\n'.format(sum(self.total))
        return out




def CreateTets():
    """
    This function creates actual test objects that are applied against the list of draws.
    :return: list
    """
    # Initialise the list
    out = [Test30()]
    # Add the next test [Yes, this could have been done in one line
    out.append(Test30Mulligan())
    # Add your own tests here...
    # out.append(<TEST>)
    # Return the tests
    return out