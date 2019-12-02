"""
parsefile.py

File to read a (detailed) Arena log, and write to "draw_database.txt" (or just "draw_database_last.txt").

Other than managing log file names and/or what directories that appear, this code is the only place that is affected
by changes to the log file format. As such, the only major source of maintenance. All other code should work
with the parsed data in draw_database.txt.


"""

import ast
import datetime

from parsercode.utils import Log as Log
import parsercode.utils as utils



def ProcessFile(filename, append_production=False, verbose=False):
    Log('Processing: ' + filename + '\n')
    f = open(filename, 'r')
    deck_handler = None
    # Metadata that needs to be added to the row
    user_name = '?'
    build = '?'
    draw_time = '?'
    match_type = '?'
    handle_last = open('draw_database_last.txt', 'a')
    # Move game info into an object. Will delete "floating variables" later.
    game_info = GameInfo()
    if append_production:
        handle_prod = open('draw_database.txt', 'a')
    else:
        handle_prod = None
    for row in f:
        # Look for the client version
        if build == '?':
            pos = row.find('\\"clientVersion\\":')
        else:
            # We have the build, ignore
            pos = -1
        if pos > -1:
            cut = row[pos:(pos+80)]
            cut = cut.split(':')
            if len(cut) > 1:
                build = cut[1]
                pos = build.find(',')
                build = build[0:pos]
                build = build.replace('"', '')
                build = build.replace('\\', '').strip()
                Log('Build = {0}\n'.format(build))

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
            Log('Found matchGameRoomStateChangedEvent; clearing GameInfo')
            game_info = GameInfo()
            try:
                match_type =  d['matchGameRoomStateChangedEvent']['gameRoomInfo']['gameRoomConfig']['eventId']
                Log('Found match type: {0}\n'.format(match_type))
                game_info.match_type = match_type
                # if deck_handler is not None:
                #     deck_handler.match_type = match_type
                #     # Clear now that it is stored in the deck
                #     match_type = '?'
            except KeyError:
                pass
            try:
                player_list = d['matchGameRoomStateChangedEvent']['gameRoomInfo']['gameRoomConfig']['reservedPlayers']
            except KeyError:
                Log('Mangled matchGameRoomStateChangedEvent event')
                continue
            for p in player_list:
                if p['playerName'] == user_name:
                    player_number = p['systemSeatId']
                    game_info.player_number = player_number
                    if deck_handler is not None:
                        deck_handler.player_number = player_number
                else:
                    game_info.other_player = p['playerName']
                    Log('Found other player: {0}\n'.format(game_info.other_player))
                    # if deck_handler is not None:
                    #     deck_handler.other_player = p['playerName']
                    #     Log('Found other player: {0}\n'.format(deck_handler.other_player))
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

        # We need see whether a new deck message has been sent.
        new_handler = FindDeck(transact, msg_list)
        if new_handler is not None:
            deck_handler = new_handler
            deck_handler.user_name = user_name
            deck_handler.file_name = filename
            deck_handler.build = build
            deck_handler.match_type = match_type
            player_number = None

        # If we have a deck handler, we can now attempt to process messages, which are mulligan responses.
        if deck_handler is not None:
            for msg in msg_list:
                deck_handler.handle_message(transact, msg, row)
            # Once we have the deck, the mulligan count, and the initial draw, that's it.
            if deck_handler.IsDone():
                if deck_handler.user_name.startswith('DeadlyK1tten'):
                    deck_handler.user_name = 'Amaz1ngK1tten'
                lline = deck_handler.Format(game_info)
                handle_last.write(lline)
                if handle_prod is not None:
                    handle_prod.write(lline)
                deck_handler.Clear()



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
            obj = DeckInfo(transact, deck)
            return obj


class GameInfo(object):
    def __init__(self):
        self.player_number = None
        self.other_player = '?'
        self.match_type = '?'


class DeckInfo(object):
    def __init__(self, transact, deck):
        self.deck = deck
        self.transact = transact
        self.file_name = '?'
        self.mulligan = None
        self.draw = None
        self.user_name = '?'
        self.player_number = None
        # Note: data will migrate to GameInfo
        self.other_player = '?'
        self.build = '?'
        self.match_type = '?'
        # Extra information to be filled in later

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
                        # Player number parsing was not working for some reason vs. Sparky, so just
                        # look at all hands. If the wrong player's hand, will get an error when
                        # we try to map object ID's. Fails in a wacky game mode where you can see opponent's
                        # hands.
                        if (z['type'] == 'ZoneType_Hand'): # and z['ownerSeatId'] == self.player_number):
                            hand = (z['objectInstanceIds'])
                            # Note: the object seems to be in reverse order. Sort by objectId, since we might
                            # eventually extend to look at draws into the library.
                            hand.sort()
                            # Log('Hand: ' + str(hand) + '\n')
                            try:
                                card_ids = [mapping[x] for x in hand]
                                Log('Card IDs: ' + str(card_ids) +'\n')
                                # Note: this will fail if they change away from the London Mulligan,
                                # or in alternate play modes. Eliminate?
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

    def Format(self, game_info):
        Log('Formating draw\n')
        draw = [str(x) for x in self.draw]
        deck = [str(x) for x in self.deck]
        cut_name = self.user_name
        # Eliminate # digits.
        pos = cut_name.find('#')
        if pos > -1:
            cut_name = cut_name[0:pos]

        row = [self.transact, self.build, cut_name, game_info.match_type, self.file_name, game_info.other_player, self.Paremeters,
               str(self.mulligan)] + draw
        row.append('-1')
        row += deck
        out = ';'.join(row)
        return out + '\n'


def GetCardDefinitions(filename, land_mapping):
    Log('Processing: ' + filename + '\n')
    f = open(filename, 'r')
    for row in f:

        # We are only looking for logged transactions, which are saved in a format that is compatible with w Python dict
        if not row.startswith('{ "transactionId":'):
            continue
        # They use true instead of True... Must be a better way of doing this, but...
        row = row.replace('true', 'True')
        row = row.replace('false', 'False')
        # This should be safe; just allows low-level Python objects, no code execution
        d = ast.literal_eval(row)

        if 'greToClientEvent' in d:
            transact = d['transactionId']
            msg_list = d['greToClientEvent']['greToClientMessages']
            # Log('Transaction: {0}\n'.format(transact))
            for msg in msg_list:
                try:
                    data = msg['gameStateMessage']['gameObjects']
                    for obj in data:
                        if obj['type'] == 'GameObjectType_Card':
                            grpId = obj['grpId']
                            is_land = 'CardType_Land' in obj['cardTypes']
                            if is_land:
                                land_mapping[grpId] = 'L'
                            else:
                                land_mapping[grpId] = 'N'
                except KeyError:
                    pass
        else:
            # Nothing to process
            continue


