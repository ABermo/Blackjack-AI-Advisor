# I have to regenerate the list as the one in blackjack.py contains hidden information (dealer's second card)
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

def aces_score(score, aces):
    while (score > 21 and aces > 0):
        aces -= 1
        score -= 10
    
    return score


def remove_seen_cards(id):
    for i in range(1,len(players[id])):
        c = players[id]["c" + str(i)]
        game_set.pop(game_set.index(c))
    
    # Remove the visible dealer card
    game_set.pop(game_set.index(players[-1]['c1']))
    


def survivability(id):
    current_score = players[id]['score']
    
    aces = 0
    if (players[id]['c1'] == 'A'):
        aces += 1
    if (players[id]['c2'] == 'A'):
        aces += 1
        
    survived = 0
    total = 0
    
    for card in game_set:
        curr_aces = aces
        curr_score = current_score + VALUES[card]
        
        if card == 'A':
            curr_aces += 1
        
        if ((curr_score > 21) and aces > 0):
            curr_score = aces_score(current_score + VALUES[card], aces)
            
        if (curr_score) <= 21:
            survived += 1
        
        total += 1
    
    print(f"You have a {survived/total:.2%} chance of surviving a hit")
    


def dealer_hitting_probability():
    current_score = VALUES[players[-1]['c1']]
    
    hits = 0
    total = 0
    survive_chance = 0
    aces = 0
    
    if (players[-1]['c1'] == 'A'):
        aces += 1
    
    for card in game_set:
        curr_aces = aces
        if card == 'A':
            curr_aces += 1
            
        if ((current_score + VALUES[card]) <= 16):
            hits += 1
            
            # Put inside the If statement as dealer don't hit if has a value of 17 or more
            survive_chance += dealer_hitting_survivability(current_score + VALUES[card], curr_aces)
        
        total += 1
    
    force_hit = hits/total
    
    if hits > 0:
        go_bust = 1 - (survive_chance / hits)
    else:
        go_bust = 0

    survive = 1 - (force_hit * go_bust)
    print(f"You should expect the dealer to be forced to hit {force_hit:.2%} of the time")
    print(f"When hitting you should expect the dealer to go bust {go_bust:.2%} of the time")
    
    print(f"Therefore you should expect the dealer to survive {survive:.2%} of the time")
    


def dealer_hitting_survivability(score, aces):
    survived = 0
    total = 0
    
    for card in game_set:
        if card == 'A':
            aces += 1
            
        current_score = score + VALUES[card]
        if (current_score > 21 and aces > 0):
            current_score = aces_score(current_score, aces)
            aces -= 1
            
        if (current_score < 17):
            survived += dealer_hitting_survivability(current_score, aces)
        elif (current_score < 22):
            survived += 1
        
        total += 1
    
    return (survived/total)
        
# Preset for testing, will be removed once linked with blackjack.py
players[1] = {'score': 15, 'c1': 'A', 'c2': 'A'}
players[-1] = {'score': 12, 'c1': '10', 'c2': '4'}

remove_seen_cards(1)
survivability(1)
dealer_hitting_probability()