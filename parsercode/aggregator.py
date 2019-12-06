"""
Code to aggregate data from tests.

Note: All tests are aggregated to the same user (last to appear). If someone got their hands on
a multi-user draw database, might need to fix.

"""

from parsercode.utils import Log as Log, format_float
import parsercode.utils as utils



class Test(object):
    def __init__(self, user):
        self.User = user

    def ProcessRow(self, user, draw, deck, mulligan_count, mode):
        pass

    def GetOutput(self):
        return ''


class Test30(Test):
    """
    30 land test: deck with 30 plains, 30 swamps, count the number of swamps.

    Only looks at initial draw, not mulligans.

    Defeats the B01 hand picker by being 100% lands. There should be no bias between swamps vs. plains.

    As a result, ignores mode.
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
        row = ['30', self.User] + [str(x) for x in self.total]
        out = ','.join(row) + '={0}\n'.format(sum(self.total))
        return out


class Test30Mulligan(Test30):
    """
    30 land test, including mulligans.

    Easy to build this up. However, not expected to have a bias based on Douglas' earlier arguments.
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


class TestAllPositions(Test):
    """
    Look at card draws versus initial position, all modes.
    """
    def __init__(self, user='?'):
        super().__init__(user)
        self.Tests = {}
        self.Mulligans = {}
        self.Ntrials = {}
        self.MullTrials = {}

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
        N = len(deck)
        self.User = user
        if N not in self.Tests:
            self.Tests[N] = [0.] * N
            self.Mulligans[N] = [0.] * N
            self.Ntrials[N] = 0
            self.MullTrials[N] = 0
        # Build a dict that maps card_id -> all positions the card appears in the deck
        mapper = {}
        if mulligan_count == 0:
            self.Ntrials[N] += 1
        self.MullTrials[N] += 1
        for pos in range(0,len(deck)):
            card_id = deck[pos]
            if card_id not in mapper:
                mapper[card_id] = []
            mapper[card_id].append(pos)
        for card_id in draw:
            appears = mapper[card_id]
            factor = 1./float(len(appears))
            for pos in appears:
                self.Mulligans[N][pos] += factor
                if mulligan_count == 0:
                    self.Tests[N][pos] += factor

    def GetOutput(self):
        n_list = list(self.Tests.keys())
        n_list.sort()
        out = ''
        for N in n_list:
            row = ['POS{0}'.format(N), self.User]
            data = [format_float(x) for x in self.Tests[N]]
            line = ','.join(row + data)
            line += '={0}\n'.format(self.Ntrials[N])
            out += line
            row = ['POS{0}MULL'.format(N), self.User]
            data = [format_float(x) for x in self.Mulligans[N]]
            line = ','.join(row + data)
            line += '={0}\n'.format(self.MullTrials[N])
            out += line
        return out

class TestLands(Test):
    """
    Look at card draws versus initial position, all modes.
    """
    def __init__(self, user='?'):
        super().__init__(user)
        self.Tests = {}
        self.Ntrials = {}
        self.rejected = 0
        self.mode_mappings = {}

    def ModeMap(self, mode):
        if mode.startswith('Play_Brawl'):
            mode = 'Brawl'
        if mode.startswith('QuickDraft_'):
            mode = 'DraftBo1'
        return mode

    def ProcessRow(self, user, draw, deck, mulligan_count, orig_mode):
        """
        As per class description, mode does not matter.
        :param user:
        :param draw:
        :param deck:
        :param mulligan_count:
        :param mode:
        :return:
        """
        N = len(deck)
        self.User = user
        if ('?' in deck) or ('?' in draw):
            self.rejected += 1
            return
        mode = self.ModeMap(orig_mode)
        if not (mode == orig_mode):
            self.mode_mappings[orig_mode] = mode
        deck_land = sum(['L' == x for x in deck])
        draw_land = sum(['L' == x for x in draw])
        test_code = '{0}:{1:02}/{2}'.format(mode, deck_land, N)
        if mulligan_count > 0:
            test_code += ':MULL'

        if test_code not in self.Tests:
            self.Tests[test_code] = [0] * 8
            self.Ntrials[test_code] = 0
        self.Tests[test_code][draw_land] += 1
        self.Ntrials[test_code] += 1

    def GetOutput(self):
        test_list = list(self.Tests.keys())
        test_list.sort()
        out = 'Number of Rejected draws/mulls = {0}\n'.format(self.rejected)
        for k in self.mode_mappings:
            out += 'Mapped Mode: {0} -> {1}\n'.format(k, self.mode_mappings[k])
        for test_code in test_list:
            row = [test_code, self.User]
            data = [str(x) for x in self.Tests[test_code]]
            line = ','.join(row + data)
            line += '={0}\n'.format(self.Ntrials[test_code])
            out += line
        return out




def run_tests(test_list):
    f = open('draw_database.txt', 'r')
    already_processed = set()
    for row in f:
        data = row.strip().split(';')
        user = data[3]
        mode = data[4]
        mulligan_count = int(data[8])
        card_info = data[(utils.draw_database_header_size):]
        card_info = [int(x) for x in card_info]

        try:
            idx = card_info.index(utils.draw_database_separator)
        except ValueError:
            Log('Row missing deck separator: {0}\n'.format(row))
            continue
        for t in test_list:
            t.ProcessRow(user, card_info[0:idx], card_info[(idx + 1):], mulligan_count, mode)
    f_out = open('summary.txt', 'w')
    for t in test_list:
        s = t.GetOutput()
        print(s)
        f_out.write(s)



def main():
    test_list = [Test30(), Test30Mulligan(), TestAllPositions()]
    run_tests(test_list)

def run_land_counts():
    """
    For now, just copy the code. Should refactor into a single function.
    :return:
    """
    f = open('land_draws.txt', 'r')
    already_processed = set()
    test_list = [TestLands()]
    for row in f:
        data = row.strip().split(';')
        user = data[3]
        mode = data[4]
        mulligan_count = int(data[8])
        card_info = data[(utils.draw_database_header_size):]
        # card_info = [int(x) for x in card_info]

        try:
            idx = card_info.index(str(utils.draw_database_separator))
        except ValueError:
            Log('Row missing deck separator: {0}\n'.format(row))
            continue
        for t in test_list:
            t.ProcessRow(user, card_info[0:idx], card_info[(idx + 1):], mulligan_count, mode)
    f_out = open('summary_land.txt', 'w')
    for t in test_list:
        s = t.GetOutput()
        print(s)
        f_out.write(s)