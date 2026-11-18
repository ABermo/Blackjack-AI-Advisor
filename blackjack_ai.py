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


def remove_seen_cards(id):
    for i in range(1,len(players[id])):
        c = players[id]["c" + str(i)]
        game_set.pop(game_set.index(c))
    
    # Remove the visible dealer card
    game_set.pop(game_set.index(players[-1]['c1']))
    


def survivability(id):
    current_score = players[id]['score']
    
    survived = 0
    total = 0
    
    for card in game_set:
        if (current_score + VALUES[card]) <= 21:
            survived += 1
        
        total += 1
    
    print(f"You have a {survived/total:.2%} chance of surviving a hit")
    


def dealer_hitting_probability():
    current_score = VALUES[players[-1]['c1']]
    
    hits = 0
    total = 0
    
    for card in game_set:
        if (current_score + VALUES[card] <= 16):
            hits += 1
        
        total += 1

    
    print(f"You should expect the dealer to be forced to hit {hits/total:.2%} of the time")
    

players[1] = {'score': 15, 'c1': '10', 'c2': '5'}
players[-1] = {'score': 12, 'c1': '8', 'c2': '4'}

remove_seen_cards(1)
survivability(1)
dealer_hitting_probability()