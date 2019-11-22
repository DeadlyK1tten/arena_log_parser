"""
utils.py

Core code.


"""

import ast
import datetime

import code.decks as decks


log_handle = None


def Log(txt):
    global log_handle
    if log_handle is None:
        log_handle = open('log.txt', 'w')
    print(txt)
    log_handle.write(txt)


def ProcessFile(filename):
    Log('Processing: ' + filename + '\n')
    f = open(filename, 'r')
    deck_handler = None
    user_name = '?'
    handle_draws = open('draws.txt', 'a')
    for row in f:
        # We are only looking for logged transactions, which are saved in a format that is compatible with w Python dict
        if not row.startswith('{ "transactionId":'):
            continue
        # They use true instead of True... Must be a better way of doing this, but...
        row = row.replace('true', 'True')
        row = row.replace('false', 'False')
        try:
            Log('Found a transaction row\n')
            Log(row + '\n')
            Log('Evaluating\n')
            # This should be safe; just allows low-level Python objects, no code execution
            d = ast.literal_eval(row)
            # Find user name if it exists
            if 'authenticateResponse' in d:
                if 'screenName' in d['authenticateResponse']:
                    user_name = d['authenticateResponse']['screenName']
                    Log('Found screen name: ' + user_name + '\n')
                    if user_name.startswith('DeadlyK1tten'):
                        user_name = 'Amaz1ngK1tten'
            if 'greToClientEvent' in d:
                transact = d['transactionId']
                msg_list = d['greToClientEvent']['greToClientMessages']
                Log('Transaction: {0}\n'.format(transact))
                # pprint.pprint(msg.keys())
            else:
                continue
        except:
            raise
        try:
            new_handler = FindDeck(transact, msg_list)
            if new_handler is not None:
                deck_handler = new_handler
                deck_handler.user_name = user_name
        except UnmatchedDeck:
            Log('Unmatched deck\n')
            deck_handler = None
        if deck_handler is not None:
            for msg in msg_list:
                deck_handler.handle_message(transact, msg, row)
            if deck_handler.IsDone():
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
            mapper = {}
            # Create a mapping from card # -> position
            for pos in range(0, len(deck)):
                mapper[deck[pos]] = pos
            if len(mapper) == len(deck):
                # Singleton if mapper has same # of entries as deck
                # TODO: Validate this logic when Brawl hits.
                if len(deck) == 59:
                    code = 'BRAWL'
                else:
                    code = 'SING' + str(len(deck))
                obj = SingletonDeck(transact, deck, code, mapper)
                return obj
            raise UnmatchedDeck('not in list')


class DeckInfo(object):
    def __init__(self, transact, deck, code):
        self.code = code
        self.deck = deck
        self.transact = transact
        self.mulligan = None
        self.draw = None
        self.user_name = '?'
        # Extra information to be filled in later: play time, opponent, build, ...

        self.Paremeters = 'PROC={0}'.format(datetime.datetime.now().isoformat(timespec='seconds'))

    def handle_message(self, transact, msg, row):
        if 'gameStateMessage' in msg and 'ClientMessageType_MulliganResp' in row:
            if 'gameStateMessage' in msg:
                Log('Found a game state message during mulligan')
                hand = []
                state_msg = msg['gameStateMessage']
                # pprint.pprint(state_msg)
                # pprint.pprint(state_msg['zones'])
                self.transact = transact
                for z in state_msg['zones']:
                    if (z['type'] == 'ZoneType_Hand' and z['ownerSeatId'] == 1):
                        hand = (z['objectInstanceIds'])
                Log(str(hand) + '\n')
                objects = state_msg['gameObjects']
                mapping= {}
                for obj in objects:
                    mapping[obj['instanceId']] = obj['grpId']
                card_ids = [mapping[x] for x in hand]
                Log('Card IDs: ' + str(card_ids) +'\n')
                self.draw = card_ids

        if 'mulliganReq' in msg:
            # mulliganCount is not defined if zero.
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

        row = [self.code, self.transact, self.user_name, self.Paremeters, str(self.mulligan)] + draw
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



def aggregate30():
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
    out_string = [str(x) for x in out]
    final = [target_code, user_name] + out_string
    f = open('summary_30.txt', 'w')
    f.write(','.join(final) + '\n')







