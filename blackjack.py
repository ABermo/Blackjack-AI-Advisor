import random as r
import blackjack_ai as ai
import time as t

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
        print(f"{players[id][i]} ", end='')
        t.sleep(0.5)
    print(f"\nGiving you a total hand value of {players[id]['score']}")
    t.sleep(0.5)
    
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



def dealer_finish(id):
    print("The dealer is holding")
    for i in range(1, len(players[-1])):
        print(players[-1]["c" + str(i)])
    print(f"Which holds a score of {players[-1]['score']}")
    
    
    while (players[-1]['score'] < 17):
        i = r.randint(0, len(game_set) - 1)
        c = game_set[i]
        game_set.pop(i)
            
        print(f"The dealer has drawn a {c}")
            
        j = "c" + str(len(players[-1]))
        players[-1][j] = c
            
        score_hand(-1)
        
        print("The dealer is holding")
        for i in range(1, len(players[-1])):
            print(players[-1]["c" + str(i)])
        print(f"Which holds a score of {players[-1]['score']}")
    win_check(id)

    

def win_check(id):
    player_score = players[id]['score']
    dealer_score = players[-1]['score']
    
    if (dealer_score > 21):
        print(f"The dealer has gone bust with {dealer_score}, you win!")
        return
    
    if (player_score == dealer_score):
        print(f"As you and the dealer both have a score of {player_score}, this game is a push and you receive your bet back")
    elif (player_score > dealer_score):
        print(f"You have beaten the dealer!")
    elif (player_score < dealer_score):
        print(f"You've lost to the dealer and lost your bet")
    
    
    
def action_input(id):
    global alive
    display(id)
    t.sleep(0.5)
    print("What would you like to do:")
    t.sleep(0.5)
    print("1. Hit")
    t.sleep(0.5)
    print("2. Stick")
    
    ai.players_take_in(players)
    ai.remove_seen_cards(id)
    t.sleep(0.5)
    hw, ht, hl = ai.hit_winning_probability(id)
    t.sleep(0.5)
    sw, st, sl = ai.stay_winning_probability(id)
    t.sleep(0.5)
    advice(hw, hl, sw, sl)
    action = input()
    
    if (action.strip().lower() in ('1', '1.', 'h', 'hit')):
        hit(id)
    elif (action.strip().lower() in ('2', '2.', 's', 'stay')):
        alive = False # This just prevents the loop from continuing forever
        print(f"You are sticking with a score of {players[id]['score']}")
        dealer_finish(id)



def advice(hw, hl, sw, sl):
    if (hw > sw):
        if (hl > sl):
            print("Looking at the numbers, you have greater odds of winning but also greater odds of losing if you decide to hit")
            print("I'd recommend that if you're here to gamble, take the hit and play the odds")
        elif (hl < sl):
            print("Your winning odds are better and your losing odds are less if you hit, to me its a no brainer, Hit")
        else:
            print("You've greater odds of winning when you hit and it doesn't affect your losing odds, so I'd advise you to Hit")
    elif (sw > hw):
        if (hl > sl):
            print("Your winning odds are better and your losing odds are less if you stay, to me its a no brainer, Stay")
        elif (hl < sl):
            print("Looking at the numbers, you have greater odds of winning but also greater odds of losing if you decide to stay")
            
player = 1
dealer = -1 # Dealer will always be -1
deal_hand(player)
deal_hand(dealer)

while alive:
    action_input(player)