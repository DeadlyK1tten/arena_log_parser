"""
Code to aggregate data from tests.

"""

from parsercode.utils import Log as Log
import parsercode.utils as utils



class Test(object):
    def __init__(self, user):
        self.User = user

    def ProcessRow(self, user, draw, deck, mulligan_count):
        pass

    def GetOutput(self):
        return ''


class Test30(Test):
    """
    30 land test: deck with 30 plains, 30 swamps, count the number of swamps.

    Only looks at initial draw, not mulligans.

    Defeats the B01 hand picker by being 100% lands. There should be no bias between swamps vs. plains.
    """
    def __init__(self, user='?'):
        super().__init__(user)
        self.total = [0] * 8
        self.target = 70405
        self.Deck = [70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70397,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405,
               70405]

    def ProcessRow(self, user, draw, deck, mulligan_count):
        if not mulligan_count == 0:
            return
        if utils.decks_equal(deck, self.Deck):
            cnt = sum([x == self.target for x in draw])
            self.User = user
            self.total[cnt] += 1

    def GetOutput(self):
        row = ['30', self.User] + [str(x) for x in self.total]
        out = ','.join(row) + '={0}\n'.format(sum(self.total))
        return out


class Test30Mulligan(Test30):
    """
    30 land test, including mulligans.

    Easy to build this up. However, not expected to have a bias based on Douglas' earlier arguments.
    """
    def ProcessRow(self, user, draw, deck, mulligan_count):
        if utils.decks_equal(deck, self.Deck):
            cnt = sum([x == self.target for x in draw])
            self.User = user
            self.total[cnt] += 1

    def GetOutput(self):
        row = ['30MULL', self.User] + [str(x) for x in self.total]
        out = ','.join(row) + '={0}\n'.format(sum(self.total))
        return out


def run_tests(test_list):
    f = open('draw_database.txt', 'r')
    already_processed = set()
    for row in f:
        data = row.strip().split(';')
        user = data[2]
        mulligan_count = int(data[7])
        card_info = data[(utils.draw_database_header_size):]
        card_info = [int(x) for x in card_info]

        try:
            idx = card_info.index(utils.draw_database_separator)
        except ValueError:
            Log('Row missing deck separator: {0}\n'.format(row))
            continue
        for t in test_list:
            t.ProcessRow(user, card_info[0:idx], card_info[(idx + 1):], mulligan_count)
    f_out = open('summary.txt', 'w')
    for t in test_list:
        s = t.GetOutput()
        print(s)
        f_out.write(s)



def main():
    test_list = [Test30(), Test30Mulligan()]
    run_tests(test_list)

