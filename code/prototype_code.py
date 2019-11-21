"""
Scratch file used to do initial testing.


"""


import os
import glob
import pprint

x = """
{ "transactionId": "d8b4f2a9-5439-40b2-9e40-a863fc9b6ccd", "timestamp": "637097814742171353", "greToClientEvent": { "greToClientMessages": [ { "type": "GREMessageType_GameStateMessage", "systemSeatIds": [ 1 ], "msgId": 7, "gameStateId": 2, "gameStateMessage": { "type": "GameStateType_Diff", "gameStateId": 2, "players": [ { "lifeTotal": 20, "systemSeatNumber": 1, "maxHandSize": 7, "teamId": 1, "timerIds": [ 1 ], "controllerSeatId": 1, "controllerType": "ControllerType_Player", "pendingMessageType": "ClientMessageType_MulliganResp", "startingLifeTotal": 20 }, { "lifeTotal": 20, "systemSeatNumber": 2, "maxHandSize": 7, "teamId": 2, "timerIds": [ 2 ], "controllerSeatId": 2, "controllerType": "ControllerType_Player", "pendingMessageType": "ClientMessageType_MulliganResp", "startingLifeTotal": 20 } ], "turnInfo": { "activePlayer": 2, "decisionPlayer": 2 }, "zones": [ { "zoneId": 31, "type": "ZoneType_Hand", "visibility": "Visibility_Private", "ownerSeatId": 1, "objectInstanceIds": [ 105, 104, 103, 102, 101, 100, 99 ], "viewers": [ 1 ] }, { "zoneId": 32, "type": "ZoneType_Library", "visibility": "Visibility_Hidden", "ownerSeatId": 1, "objectInstanceIds": [ 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158 ] }, { "zoneId": 35, "type": "ZoneType_Hand", "visibility": "Visibility_Private", "ownerSeatId": 2, "objectInstanceIds": [ 225, 224, 223, 222, 221, 220, 219 ], "viewers": [ 2 ] }, { "zoneId": 36, "type": "ZoneType_Library", "visibility": "Visibility_Hidden", "ownerSeatId": 2, "objectInstanceIds": [ 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278 ] } ], "gameObjects": [ { "instanceId": 99, "grpId": 70405, "type": "GameObjectType_Card", "zoneId": 31, "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, "superTypes": [ "SuperType_Basic" ], "cardTypes": [ "CardType_Land" ], "subtypes": [ "SubType_Swamp" ], "viewers": [ 1 ], "name": 653, "abilities": [ 1003 ], "overlayGrpId": 70405 }, { "instanceId": 100, "grpId": 70397, "type": "GameObjectType_Card", "zoneId": 31, "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, "superTypes": [ "SuperType_Basic" ], "cardTypes": [ "CardType_Land" ], "subtypes": [ "SubType_Plains" ], "viewers": [ 1 ], "name": 648, "abilities": [ 1001 ], "overlayGrpId": 70397 }, { "instanceId": 101, "grpId": 70405, "type": "GameObjectType_Card", "zoneId": 31, "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, "superTypes": [ "SuperType_Basic" ], "cardTypes": [ "CardType_Land" ], "subtypes": [ "SubType_Swamp" ], "viewers": [ 1 ], "name": 653, "abilities": [ 1003 ], "overlayGrpId": 70405 }, { "instanceId": 102, "grpId": 70405, "type": "GameObjectType_Card", "zoneId": 31, "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, "superTypes": [ "SuperType_Basic" ], "cardTypes": [ "CardType_Land" ], "subtypes": [ "SubType_Swamp" ], "viewers": [ 1 ], "name": 653, "abilities": [ 1003 ], "overlayGrpId": 70405 }, { "instanceId": 103, "grpId": 70405, "type": "GameObjectType_Card", "zoneId": 31, "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, "superTypes": [ "SuperType_Basic" ], "cardTypes": [ "CardType_Land" ], "subtypes": [ "SubType_Swamp" ], "viewers": [ 1 ], "name": 653, "abilities": [ 1003 ], "overlayGrpId": 70405 }, { "instanceId": 104, "grpId": 70397, "type": "GameObjectType_Card", "zoneId": 31, "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, "superTypes": [ "SuperType_Basic" ], "cardTypes": [ "CardType_Land" ], "subtypes": [ "SubType_Plains" ], "viewers": [ 1 ], "name": 648, "abilities": [ 1001 ], "overlayGrpId": 70397 }, { "instanceId": 105, "grpId": 70397, "type": "GameObjectType_Card", "zoneId": 31, "visibility": "Visibility_Private", "ownerSeatId": 1, "controllerSeatId": 1, "superTypes": [ "SuperType_Basic" ], "cardTypes": [ "CardType_Land" ], "subtypes": [ "SubType_Plains" ], "viewers": [ 1 ], "name": 648, "abilities": [ 1001 ], "overlayGrpId": 70397 } ], "annotations": [ { "id": 2018, "affectorId": 2, "affectedIds": [ 2 ], "type": [ "AnnotationType_NewTurnStarted" ] } ], "diffDeletedInstanceIds": [ 219, 220, 221, 222, 223, 224, 225 ], "prevGameStateId": 1, "timers": [ { "timerId": 2, "type": "TimerType_Inactivity", "durationSec": 1020, "running": true, "behavior": "TimerBehavior_Timeout", "warningThresholdSec": 990, "elapsedMs": 4 } ], "update": "GameStateUpdate_SendAndRecord", "actions": [ { "seatId": 1, "action": { "actionType": "ActionType_Play", "instanceId": 100 } }, { "seatId": 1, "action": { "actionType": "ActionType_Play", "instanceId": 104 } }, { "seatId": 1, "action": { "actionType": "ActionType_Play", "instanceId": 105 } }, { "seatId": 1, "action": { "actionType": "ActionType_Play", "instanceId": 101 } }, { "seatId": 1, "action": { "actionType": "ActionType_Play", "instanceId": 99 } }, { "seatId": 1, "action": { "actionType": "ActionType_Play", "instanceId": 102 } }, { "seatId": 1, "action": { "actionType": "ActionType_Play", "instanceId": 103 } } ] } } ] } }
"""

true = True
false = False
y = eval(x)

# print(y)

target_deck = [70397,
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

def main():
    print('Start')
    f = open('output_log.txt', 'r')
    hand = []
    for row in f:
        if not row.startswith('{ "transactionId":'):
            continue
        try:
            d = eval(row)
            if 'greToClientEvent' in d:
                transact = d['transactionId']
                msg_list = d['greToClientEvent']['greToClientMessages']
                print('Transaction:', transact)
                # pprint.pprint(msg.keys())
            else:
                continue
        except:
            continue
        for msg in msg_list:
            if 'connectResp' in msg: #'GREMessageType_ConnectResp' in row:
                print('*1' * 80)
                # d = eval(row)
                # pprint.pprint(d)
                # llist = d['greToClientEvent']['greToClientMessages']
                # print(llist[0].keys())
                # print(llist[0]['connectResp'].keys())
                deck_message = msg['connectResp']['deckMessage']
                print(deck_message)
                hand = []
            if 'gameStateMessage' in msg and 'ClientMessageType_MulliganResp' in row:
                print('*2' * 80)
                if 'gameStateMessage' in msg:
                    state_msg = msg['gameStateMessage']
                    # pprint.pprint(state_msg)
                    # pprint.pprint(state_msg['zones'])
                    for z in state_msg['zones']:
                        if (z['type'] == 'ZoneType_Hand' and z['ownerSeatId'] == 1):
                            hand = (z['objectInstanceIds'])
                    print(hand)
                    objects = state_msg['gameObjects']
                    mapinator = {}
                    for obj in objects:
                        mapinator[obj['instanceId']] = obj['grpId']
                    card_ids = [mapinator[x] for x in hand]
                    print(card_ids)
                # for k in state_msg.keys():
                #     print('*' * 20, k)
                #     pprint.pprint(state_msg[k])
                # print('=' * 80)
                # pprint.pprint(second_msg)
            if False: #'prompt' in msg:
                try:
                    num_cards = msg['prompt']['parameters'][0]['numberValue']
                except KeyError:
                    # print('Not a mulligan')
                    continue
                print('Number of cards = ', num_cards)
            if 'mulliganReq' in msg:
                mulligan_count = msg['mulliganReq'].get('mulliganCount', 0)
                print('Mulligan count =', mulligan_count)
        if False: # 'mulliganReq' in row:
            print('*3' * 80)
            print(row[0:20])
            pprint.pprint(msg)
            print(msg.keys())
            break



if __name__ == '__main__':
    main()