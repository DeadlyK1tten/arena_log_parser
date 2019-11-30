"""
utils.py

Core code.


"""

import ast
import datetime
import os

import parsercode.decks as decks


log_handle = None


def SetWorkingDirectory(base_file):
    """
    Set the working directory to match that of a target file. Used by scripts to eliminate issues from
    different invocation points.
    :param base_file: str
    :return:
    """
    os.chdir(os.path.dirname(base_file))

def ArchiveUTClog(original):
    base = os.path.basename(original)
    target = os.path.join('UTC_logs', 'parsed', base)
    os.rename(original, target)

def Log(txt):
    global log_handle
    if log_handle is None:
        log_handle = open('log.txt', 'w')
    print(txt)
    log_handle.write(txt)


def ProcessFile(filename, debug = False, verbose=False):
    """
    Go through file, line by line.

    All the information we need (?) are stored in what are almost Python dict objects converted to a single line
    text representation. That is all we are looking for.

    :param filename:
    :param debug:
    :param verbose:
    :return:
    """
    Log('Processing: ' + filename + '\n')
    f = open(filename, 'r')
    deck_handler = None
    user_name = '?'
    if debug:
        handle_draws = open('draws_debug.txt', 'a')
    else:
        handle_draws = open('draws.txt', 'a')
    for row in f:
        # We are only looking for logged transactions, which are saved in a format that is compatible with w Python dict
        if not row.startswith('{ "transactionId":'):
            continue
        # They use true instead of True... Must be a better way of doing this, but...
        row = row.replace('true', 'True')
        row = row.replace('false', 'False')
        if verbose:
            Log('Found a transaction row\n')
            Log(row + '\n')
            Log('Evaluating\n')
        # This should be safe; just allows low-level Python objects, no code execution
        d = ast.literal_eval(row)
        # We need to get some initial information in early "transactions"
        # Find user name if it exists
        if 'authenticateResponse' in d:
            if 'screenName' in d['authenticateResponse']:
                user_name = d['authenticateResponse']['screenName']
                Log('Found screen name: ' + user_name + '\n')
        # This message tells us what players are in the game. We need this
        # information to get the player ID ("systemSeatId"). The deck will have already been found,
        # or otherwise we cannot tell what is going on.
        if 'matchGameRoomStateChangedEvent' in d:
            try:
                player_list = d['matchGameRoomStateChangedEvent']['gameRoomInfo']['gameRoomConfig']['reservedPlayers']
            except KeyError:
                Log('Mangled matchGameRoomStateChangedEvent event')
                continue
            for p in player_list:
                if p['playerName'] == user_name:
                    player_number = p['systemSeatId']
                    if deck_handler is not None:
                        deck_handler.player_number = player_number
        # greToClientEvents are broadcast messages. Includes the deck list.
        # Can split information between multiple "messages" within the transaction.
        if 'greToClientEvent' in d:
            transact = d['transactionId']
            msg_list = d['greToClientEvent']['greToClientMessages']
            Log('Transaction: {0}\n'.format(transact))
            # pprint.pprint(msg.keys())
        else:
            # Nothing to process
            continue
        try:
            # We need see whether a new deck message has been sent.
            new_handler = FindDeck(transact, msg_list)
            if new_handler is not None:
                deck_handler = new_handler
                deck_handler.user_name = user_name
                player_number = None
        except UnmatchedDeck:
            Log('Unmatched deck\n')
            deck_handler = None
        # If we have a deck handler, we can now attempt to process messages, which are mulligan responses.
        if deck_handler is not None:
            for msg in msg_list:
                deck_handler.handle_message(transact, msg, row)
            # Once we have the deck, the mulligan count, and the initial draw, that's it.
            if deck_handler.IsDone():
                if deck_handler.user_name.startswith('DeadlyK1tten'):
                    deck_handler.user_name = 'Amaz1ngK1tten'
                deck_handler.Write(handle_draws)
                deck_handler.Clear()


def decks_equal(d1, d2):
    if not (len(d1) == len(d2)):
        return False
    for x,y in zip(d1,d2):
        if not x == y:
            return False
    return True

class UnmatchedDeck(Exception):
    pass

def FindDeck(transact, msg_list):
    """
    Returns None if not a deck message.
    :param transact:
    :param msg_list:
    :return:
    """
    for msg in msg_list:
        if 'connectResp' in msg:
            try:
                deck = msg['connectResp']['deckMessage']['deckCards']
                Log('Found Deck in new game connection')
                Log(str(deck) + '\n')
            except KeyError:
                return
            for target in decks.target_decks:
                t_deck = target['deck']
                deck_code = target['code']
                if decks_equal(deck, t_deck):
                    obj = DeckInfo(transact, deck, deck_code)
                    return obj
            # Is it Singleton?
            Log('Looking for singleton status\n')
            mapper = {}
            repeats = set()
            # Create a mapping from card # -> position
            for pos in range(0, len(deck)):
                if deck[pos] in mapper:
                    repeats.add(deck[pos])
                mapper[deck[pos]] = pos
            if len(mapper) == len(deck):
                # Singleton if mapper has same # of entries as deck
                if len(deck) == 59:
                    code = 'BRAWL'
                else:
                    code = 'SING' + str(len(deck))
                obj = SingletonDeck(transact, deck, code, mapper)
                return obj
            else:
                Log('Had repeated cards\n')
                Log(str(repeats) + '\n')
            raise UnmatchedDeck('not in list')


class DeckInfo(object):
    def __init__(self, transact, deck, code):
        self.code = code
        self.deck = deck
        self.transact = transact
        self.mulligan = None
        self.draw = None
        self.user_name = '?'
        self.player_number = None
        # Extra information to be filled in later: play time, opponent, build, ...

        self.Paremeters = 'PROC={0}'.format(datetime.datetime.now().isoformat(timespec='seconds'))

    def handle_message(self, transact, msg, row):
        if 'gameStateMessage' in msg and 'ClientMessageType_MulliganResp' in row:
            if 'gameStateMessage' in msg:
                Log('Found a game state message during mulligan\n')
                hand = []
                state_msg = msg['gameStateMessage']
                # pprint.pprint(state_msg)
                # pprint.pprint(state_msg['zones'])
                self.transact = transact
                if 'gameObjects' in state_msg:
                    objects = state_msg['gameObjects']
                    mapping = {}
                    for obj in objects:
                        mapping[obj['instanceId']] = obj['grpId']
                    for z in state_msg['zones']:
                        if (z['type'] == 'ZoneType_Hand'): # and z['ownerSeatId'] == self.player_number):
                            hand = (z['objectInstanceIds'])
                            # Log('Hand: ' + str(hand) + '\n')
                            try:
                                card_ids = [mapping[x] for x in hand]
                                Log('Card IDs: ' + str(card_ids) +'\n')
                                if not len(card_ids) == 7:
                                    Log('Logic error - initial draw does not have 7 cards.')
                                else:
                                    self.draw = card_ids
                            except KeyError:
                                # Opponent's hand, can't map
                                pass

        if 'mulliganReq' in msg:
            # mulliganCount is not defined if zero. get(x,0) returns 0, if the key "x" does not exist.
            self.mulligan = msg['mulliganReq'].get('mulliganCount', 0)
            Log('Found mulligan count = {0}\n'.format(self.mulligan))

    def IsDone(self):
        return (self.mulligan is not None) and (self.draw is not None)

    def Clear(self):
        self.mulligan = None
        self.draw = None

    def Write(self, f):
        Log('Writing draw')
        draw = [str(x) for x in self.draw]
        deck = [str(x) for x in self.deck]
        cut_name = self.user_name
        # Eliminate # digits.
        pos = cut_name.find('#')
        if pos > -1:
            cut_name = cut_name[0:pos]
        row = [self.code, self.transact, cut_name, self.Paremeters, str(self.mulligan)] + draw
        row.append('-1')
        row += deck
        out = ';'.join(row)
        f.write(out + '\n')


class SingletonDeck(DeckInfo):
    def __init__(self, transact, deck, code, mapper):
        super().__init__(transact, deck, code)
        self.Mapping = mapper

    def Write(self, f):
        Log('Writing draw')
        positions = [str(self.Mapping[x]) for x in self.draw]
        draw = [str(x) for x in self.draw]
        deck = [str(x) for x in self.deck]

        row = [self.code, self.transact, self.user_name, self.Paremeters, str(self.mulligan)] + positions
        row.append('-1')
        row += draw
        row.append('-2')
        row += deck
        out = ';'.join(row)
        f.write(out + '\n')


def aggregate():
    f = open('summary.txt', 'w')
    aggregate30(f)
    aggregate_singleton(f)


def aggregate30(f_out=None):
    """
    Minimal implementation of an aggregation, looking for the "30" test.
    :return:
    """
    target_code = "30"
    target = None
    for x in decks.target_decks:
        if x['code'] == target_code:
            target = x['target_card']
            # Leave everything a string
            target = str(target)

    f = open('draws.txt')
    already_processed = set()
    out = [0] * 8
    user_name = '?'
    for row in f:
        data = row.split(';')
        if len(data) < 10:
            continue
        [row_code, transact, user_name, params, mulligan] = data[0:5]
        hand = data[5:12]
        if not row_code == target_code:
            continue
        if transact in already_processed:
            continue
        already_processed.add(transact)
        if not int(mulligan) == 0:
            continue
        matched = [x == target for x in hand]
        count = sum(matched)
        print(count)
        out[count] += 1
    # convert to a string
    trials = sum(out)
    out_string = [str(x) for x in out]
    final = [target_code, user_name] + out_string
    if f_out is None:
        f_out = open('summary_30.txt', 'w')
    f_out.write(','.join(final) + '={0}\n'.format(trials))


def aggregate_singleton(f_out = None):
    """
    Aggregation
    :return:
    """
    summaries = {
        'SING60': [0] *60,
        'BRAWL': [0] * 59,
    }
    f = open('draws.txt')
    already_processed = set()
    out = [0] * 8
    user_name = '?'
    for row in f:
        data = row.split(';')
        if len(data) < 10:
            continue
        [row_code, transact, user_name, params, mulligan] = data[0:5]
        hand = data[5:12]
        if not row_code in summaries:
            continue
        if transact in already_processed:
            continue
        already_processed.add(transact)
        if not int(mulligan) == 0:
            continue
        for pos in hand:
            summaries[row_code][int(pos)] += 1
    if f_out is None:
        f_out = open('summary_singleton.txt', 'w')
    for k in summaries.keys():
        trials = int(sum(summaries[k])/7)
        if trials == 0:
            continue
        # convert to a string
        out_string = [str(x) for x in summaries[k]]
        final = [k, user_name] + out_string
        f_out.write(','.join(final) + '={0}\n'.format(trials))

class TrialData(object):
    def __init__(self, user, n, vector):
        self.user = user
        self.n = n
        self.vector = vector

def SumUpAllUserData(fname):
    f = open(fname, 'r')
    Log('Summing up trials')
    summaries = {}
    tests_dictionary = {}
    for row in f:
        pos = row.find('%')
        if pos > -1:
            row = row[0:pos]
        row = row.strip()
        data = row.split(',')
        if len(data) < 3:
            continue
        test = data[0]
        user = data[1]
        pos = user.find('#')
        if pos > -1:
            user = user[0:pos]
        vector = data[2:]
        # Remove any "=n" text from last entry
        pos = vector[-1].find('=')
        if pos > -1:
            vector[-1] = vector[-1][0:pos]
        try:
            vector_numeric = [int(x) for x in vector]
        except:
            Log('Could not parse data in row: \n')
            Log(row + '\n')
            continue
        n = sum(vector_numeric)
        if test in ('SING60', 'BRAWL'):
            if not n % 7 == 0:
                Log(row)
                raise ValueError('Summary with incorrect card counts (see log)')
            n = int(n /7)
        trial_data = TrialData(user, n, vector_numeric)
        kkey = (test, user)
        if kkey in summaries:
            other = summaries[kkey]
            if trial_data.n > other.n:
                Log('Replacing smaller trial data {0}, {1}\n'.format(test, user))
                summaries[kkey] = trial_data
            else:
                Log('lower trial count summary, ignored {0},{1}\n'.format(test, user))
        else:
            Log('New entry: {0},{1}\n'.format(test, user))
            summaries[kkey] = trial_data
            if test in tests_dictionary:
                tests_dictionary[test].append(user)
            else:
                tests_dictionary[test] = [user]
    test_list = list(tests_dictionary.keys())
    test_list.sort()
    f_out = open('summary_all_users.txt', 'w')
    for test in test_list:
        f_out.write('Test: {0}\n'.format(test))
        users = tests_dictionary[test]
        total = None
        N = 0
        for user in users:
            k = (test, user)
            trial_data = summaries[k]
            if total is None:
                total = trial_data.vector
                N += trial_data.n
            else:
                if not len(trial_data.vector) == len(total):
                    raise ValueError('Data for user {0} for test {1} is not same length\n'.format(user, test))
                N += trial_data.n
                total = [x+y for x,y in zip(total, trial_data.vector)]
        f_out.write('Number of users: {0}\n'.format(len(users)))
        f_out.write('Number of trials: {0}\n'.format(N))
        f_out.write('Distribution\n')
        t_s = [str(x) for x in total]
        f_out.write('{0}\n'.format(', '.join(t_s)))








