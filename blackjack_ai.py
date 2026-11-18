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

# Count of each card the player hasn't seen yet (includes the dealer's hidden card)
game_set = {card: 4 for card in VALUES}

# Remembers dealer results so each situation is only worked out once per turn
dealer_cache = {}


def players_take_in(p):
    global players
    players = p


def add_card(score, aces, card):
    # Adds a card to a hand, aces = number of aces still counted as 11
    score += VALUES[card]
    if card == 'A':
        aces += 1
    
    while (score > 21 and aces > 0):
        score -= 10
        aces -= 1
    
    return score, aces


def hand_state(id):
    score = 0
    aces = 0
    
    for i in range(1, len(players[id])):
        score, aces = add_card(score, aces, players[id]["c" + str(i)])
    
    return score, aces


def remove_seen_cards(id):
    # Rebuild from scratch every turn so cards are never removed twice
    global game_set, dealer_cache
    game_set = {card: 4 for card in VALUES}
    dealer_cache = {}
    
    for i in range(1, len(players[id])):
        game_set[players[id]["c" + str(i)]] -= 1
    
    # Remove the visible dealer card
    game_set[players[-1]['c1']] -= 1


def survivability(id):
    current_score, aces = hand_state(id)
    total = sum(game_set.values())
    survived = 0
    
    for card, count in game_set.items():
        new_score, new_aces = add_card(current_score, aces, card)
        if new_score <= 21:
            survived += count
    
    print(f"You have a {survived/total:.2%} chance of surviving a hit")


def dealer_final_probability(dealer_score, aces):
    # Returns chances of the dealer finishing on [17, 18, 19, 20, 21, bust]
    key = (dealer_score, aces)
    if key in dealer_cache:
        return dealer_cache[key]
    
    result = [0, 0, 0, 0, 0, 0]
    
    if dealer_score > 21:
        result[5] = 1
    elif dealer_score >= 17:
        result[dealer_score - 17] = 1
    else:
        total = sum(game_set.values())
        
        for card, count in game_set.items():
            new_score, new_aces = add_card(dealer_score, aces, card)
            chances = dealer_final_probability(new_score, new_aces)
            
            for i in range(6):
                result[i] += chances[i] * count / total
    
    dealer_cache[key] = result
    return result


def outcome(player_score, dealer_chances):
    # Turns the dealer's final chances into (wins, draws, losses) for a player score
    if player_score > 21:
        return (0, 0, 1)
    
    wins = dealer_chances[5] # Dealer bust
    draws = 0
    losses = 0
    
    for i in range(5):
        dealer_score = 17 + i
        if player_score > dealer_score:
            wins += dealer_chances[i]
        elif player_score == dealer_score:
            draws += dealer_chances[i]
        else:
            losses += dealer_chances[i]
    
    return (wins, draws, losses)


def hit_winning_probability(id):
    current_score, aces = hand_state(id)
    dealer_score, dealer_aces = add_card(0, 0, players[-1]['c1'])
    dealer_chances = dealer_final_probability(dealer_score, dealer_aces)
    
    total = sum(game_set.values())
    wins = 0
    draws = 0
    losses = 0
    
    for card, count in game_set.items():
        player_score, player_aces = add_card(current_score, aces, card)
        w, d, l = outcome(player_score, dealer_chances)
        
        chance = count / total
        wins += w * chance
        draws += d * chance
        losses += l * chance
    
    print(f"You have a {wins:.2%} chance of winning if you hit")
    print(f"You have a {draws:.2%} chance of drawing if you hit")
    print(f"You have a {losses:.2%} chance of losing if you hit")


def stay_winning_probability(id):
    current_score, aces = hand_state(id)
    dealer_score, dealer_aces = add_card(0, 0, players[-1]['c1'])
    dealer_chances = dealer_final_probability(dealer_score, dealer_aces)
    
    wins, draws, losses = outcome(current_score, dealer_chances)
    
    print(f"You have a {wins:.2%} chance of winning if you stay")
    print(f"You have a {draws:.2%} chance of drawing if you stay")
    print(f"You have a {losses:.2%} chance of losing if you stay")