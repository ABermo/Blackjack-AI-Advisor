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

def score_hand(id):
    score = 0
    aces = 0
    
    for i in range(1, len(players[id])):
        i = "c" + str(i) # Convert to column name, c1, c2 etc
        score += VALUES[players[id][i]]
        
        if (players[id][i] == 'A'):
            aces += 1
    
    while(score > 21 and aces > 0):
        score -= 10
        aces -= 1
        
    players[id]["score"] = score

def deal_hand(id):
    i = r.randint(0, len(game_set))
    c1 = game_set[i]
    game_set.pop(i)
    
    i = r.randint(0, len(game_set))
    c2 = game_set[i]
    game_set.pop(i)
    
    
    hand = {"score": 0, "c1": c1, "c2": c2}
    players[id] = hand
    
    score_hand(id)

player = 1
deal_hand(1)
print(players[1])