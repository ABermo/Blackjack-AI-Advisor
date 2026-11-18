from functools import lru_cache


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
        
        if ((curr_score > 21) and curr_aces > 0):
            curr_score = aces_score(current_score + VALUES[card], curr_aces)
            
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
    #print(f"You should expect the dealer to be forced to hit {force_hit:.2%} of the time")
    #print(f"When hitting you should expect the dealer to go bust {go_bust:.2%} of the time")
    
    #print(f"Therefore you should expect the dealer to survive {survive:.2%} of the time")
    return survive
    

@lru_cache(maxsize=None)
def dealer_hitting_survivability(score, aces):
    survived = 0
    total = 0
    
    for card in game_set:
        curr_aces = aces
        if card == 'A':
            curr_aces += 1
            
        current_score = score + VALUES[card]
        if (current_score > 21 and curr_aces > 0):
            current_score = aces_score(current_score, curr_aces)
            curr_aces -= 1
            
        if (current_score < 17):
            survived += dealer_hitting_survivability(current_score, curr_aces)
        elif (current_score < 22):
            survived += 1
        
        total += 1
    
    return (survived/total)




def dealer_final_probability(player_score, dealer_score, aces):
    wins = 0
    draws = 0
    losses = 0
    total = 0

    if dealer_score >= 17:
        if dealer_score > 21 or player_score > dealer_score:
            return (1, 0, 0)
        elif player_score == dealer_score:
            return (0, 1, 0)
        else:
            return (0, 0, 1)

    for card in game_set:
        curr_aces = aces

        if card == 'A':
            curr_aces += 1

        current_score = dealer_score + VALUES[card]

        while current_score > 21 and curr_aces > 0:
            current_score -= 10
            curr_aces -= 1

        w, d, l = dealer_final_probability(
            player_score, current_score, curr_aces
        )

        wins += w
        draws += d
        losses += l
        total += 1

    return (wins/total, draws/total, losses/total)


def hit_winning_probability(id):
    current_score = players[id]['score']
    player_aces = 0

    if players[id]['c1'] == 'A':
        player_aces += 1
    if players[id]['c2'] == 'A':
        player_aces += 1

    dealer_score = VALUES[players[-1]['c1']]
    dealer_aces = 0

    if players[-1]['c1'] == 'A':
        dealer_aces += 1

    wins = 0
    draws = 0
    losses = 0
    total = len(game_set)

    for card in game_set:
        curr_aces = player_aces

        if card == 'A':
            curr_aces += 1

        player_score = aces_score(current_score + VALUES[card], curr_aces)

        if player_score > 21:
            losses += total
        else:
            for hidden_card in game_set:
                curr_dealer_aces = dealer_aces

                if hidden_card == 'A':
                    curr_dealer_aces += 1

                new_dealer_score = dealer_score + VALUES[hidden_card]

                if new_dealer_score > 21 and curr_dealer_aces > 0:
                    new_dealer_score = aces_score(new_dealer_score, curr_dealer_aces)

                w, d, l = dealer_final_probability(
                    player_score, new_dealer_score, curr_dealer_aces
                )

                wins += w
                draws += d
                losses += l

    total_outcomes = total * total

    wins /= total_outcomes
    draws /= total_outcomes
    losses /= total_outcomes

    print(f"You have a {wins:.2%} chance of winning if you hit")
    print(f"You have a {draws:.2%} chance of drawing if you hit")
    print(f"You have a {losses:.2%} chance of losing if you hit")



def stay_winning_probability(id):
    curr_score = players[id]['score']
    dealer_score = players[-1]['score']

    if (curr_score == 21):
        if (dealer_score == 21):
            print("You both have 21, so its a tie")
        else:
            print("You have a {1:.0%} chance of winning if you stay")
            print("You have a {0:.0%} chance of losing if you stay")

    elif (curr_score < 21):
        dealer_survive = dealer_hitting_probability()
        dealer_bust = 1 - dealer_survive

        if (curr_score < 17):
            wins = dealer_bust
        else:
            wins = dealer_bust

        loses = dealer_survive
        print(f"You have a {wins:.2%} chance of winning if you stay")
        print(f"You have a {loses:.2%} chance of losing if you stay")
    
# Preset for testing, will be removed once linked with blackjack.py
players[1] = {'score': 12, 'c1': '10', 'c2': '2'}
players[-1] = {'score': 19, 'c1': '9', 'c2': '10'}

remove_seen_cards(1)

hit_winning_probability(1)
stay_winning_probability(1)
