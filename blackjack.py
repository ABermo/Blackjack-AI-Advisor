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
alive = True



def score_hand(id):
    score = 0
    aces = 0
    
    for i in range(1, len(players[id])):
        i = "c" + str(i) # Convert to column name, c1, c2 etc
        score += VALUES[players[id][i]]
        
        if (players[id][i] == 'A'):
            aces += 1 # Counting Aces so if player goes over 21, we can take away 10
    
    while(score > 21 and aces > 0):
        score -= 10
        aces -= 1
        
    players[id]["score"] = score



def deal_hand(id):
    i = r.randint(0, len(game_set) - 1)
    c1 = game_set[i]
    game_set.pop(i)
    
    i = r.randint(0, len(game_set) - 1)
    c2 = game_set[i]
    game_set.pop(i)
    
    
    hand = {"score": 0, "c1": c1, "c2": c2}
    players[id] = hand
    
    score_hand(id)



def display(id):
    print(f"You are currently holding onto")
    for i in range(1, len(players[id])):
        i = "c" + str(i) # Check dictionary column
        print(f"{players[id][i]}")
    print(f"Giving you a total hand value of {players[id]['score']}")
    
    # Check for Dealer 21
    if (players[-1]["score"] == 21):
        print(f"The dealer is showing {players[-1]['c1']}")
    elif (players[-1]['c1'] in ('10', 'J', 'Q', 'K', 'A')):
        print(f"While the dealer is currently showing a {players[-1]['c1']} but doesn't have Blackjack")
    else:
        print(f"While the dealer is currently showing a {players[-1]['c1']}")



def bust_check(id):
    global alive
    if (players[id]["score"] > 21):
        print("You've gone over 21 and have lost on this hand")
        alive = False


def hit(id):
    print("You have chosen to hit")
    
    # Draw a random card
    i = r.randint(0, len(game_set) - 1)
    c = game_set[i]
    game_set.pop(i)
    
    print(f"You have a drawn a {c}")
    
    j = "c" + str(len(players[id]))
    players[id][j] = c
    
    score_hand(id)
    
    print(f"This now puts your score at {players[id]['score']}")
    bust_check(id)



def action_input(id):
    display(id)
    print("What would you like to do:")
    print("1. Hit")
    print("2. Stick")
    
    action = input()
    
    if (action.strip().lower() in ('1', '1.', 'h', 'hit')):
        hit(id)
        if alive:
            display(id)

player = 1
dealer = -1 # Dealer will always be -1
deal_hand(player)
deal_hand(dealer)

while alive:
    action_input(player)