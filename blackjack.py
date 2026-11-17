import random as r

BASE_CARDS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] * 4

game_set = BASE_CARDS.copy()

VALUES = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 11 # Ace given value of 11 as we can then subtract 10 from score if necessary
}

players = {}

def deal_hand(id):
    score = 0 # to make into function
    
    i = r.randint(0, len(game_set))
    c1 = game_set[i]
    game_set.pop(i)
    
    i = r.randint(0, len(game_set))
    c2 = game_set[i]
    game_set.pop(i)
    
    
    hand = {"c1": c1, "c2": c2, "score": score}
    players[id] = hand
