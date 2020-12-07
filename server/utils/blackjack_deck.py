import random
import os
import requests

# output for reference:
#{
#    'jsonrpc': '2.0',
#    'result': {
#        'random': {
#            'data': [
#                [
#                    199, 100, 59, 55, 94, 191, 181, 39, 131, 176, 19, 192, 185,
#                    5, 186, 156, 6, 83, 142, 158, 18, 135, 165, 146, 60, 25, 98, 68,
#                    109, 116, 175, 163, 65, 75, 187, 91, 201, 80, 72, 141, 7, 184, 171,
#                    126, 119, 204, 112, 151, 34, 93, 31, 127, 53, 205, 172, 182, 95, 189,
#                    1, 190, 139, 64, 168, 27, 99, 167, 21, 147, 174, 149, 206, 129, 35,
#                    81, 42, 97, 160, 12, 117, 128, 61, 195, 24, 43, 155, 36, 23, 86,
#                    32, 85, 198, 138, 79, 101, 143, 38, 9, 28, 58, 137, 111, 26, 73,
#                    107, 30, 46, 152, 49, 16, 179, 136, 169, 177, 170, 188, 120, 121, 166,
#                    114, 118, 123, 161, 200, 84, 90, 78, 140, 70, 104, 103, 193, 89, 88,
#                    17, 71, 67, 96, 77, 3, 157, 20, 8, 52, 196, 133, 56, 113, 164, 203, 132, 148,
#                    130, 57, 153, 62, 102, 162, 180, 150, 173, 178, 66, 124, 47, 14, 208,
#                    11, 134, 87, 63, 51, 159, 33, 37, 183, 44, 106, 122, 13, 41, 105,
#                    54, 15, 92, 115, 144, 76, 202, 125, 197, 2, 207, 29, 10, 50, 74,
#                    82, 194, 145, 154, 22, 108, 40, 69, 45, 4, 48, 110
#                ]
#            ],
#            'completionTime': '2020-11-19 03:20:51Z'
#        },
#        'bitsUsed': 1602,
#        'bitsLeft': 247214,
#        'requestsLeft': 998,
#        'advisoryDelay': 1500
#    },
#    'id': 490
#}

RANDOM_ORG_KEY = os.getenv("RANDOM_ORG_KEY", "DEFAULT_KEY")
RANDOM_URL = "https://api.random.org/json-rpc/2/invoke"
suits = ["D", "H", "C", "S"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K"]

def translate_hand(hand):
    lst = []
    for num in hand:
        lst.append(values[num % 13])
        lst.append(suits[num % 4])
    return lst

def blackjack_total(hand):
    total = 0
    aces = []
    for num in hand:
        if num % 13 == 0:
            aces.append(num)
        elif (num % 13) + 1 > 10:
            total += 10
        else:
            total += (num % 13) + 1
    for _ in range(len(aces)):
        if total + 11 <= 21:
            total += 11
        else:
            total += 1
    return total

def local_deck_set():
    deck = list(range(0,208))
    random.shuffle(deck)
    return deck

def get_deck_set():
    json_rpc = {
        "jsonrpc": "2.0",
        "method": "generateIntegerSequences",
        "params": {
            "apiKey": RANDOM_ORG_KEY,
            "n": 1,
            "length": 208,
            "min": 0,
            "max": 207,
        "replacement": False,
        "base": 10
        },
        "id": 490
    }
    random_request = requests.post(RANDOM_URL, json=json_rpc)
    data = random_request.json()
    if "error" in data:
        return local_deck_set()
    return data["result"]["random"]["data"][0]

def draw_card(deck):
    return deck.pop(0)
