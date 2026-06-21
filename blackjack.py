# Card Setup

BASE_CARDS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def deck_count(deck):
    cards = deck * 4 * BASE_CARDS
    return cards

deck = 1
cards = deck_count(deck)



# Scoring

SCORING = {
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
    'A': 11  # If score goes over 21 but contains 11, you can remove 10 from the scoring for A = 1
}

def convert(hand):
    for card in range(len(hand)):
        hand[card] = SCORING[hand[card]]
    
    # Ace Check
    if hand_value(hand) > 21 and 11 in hand:
        hand[hand.index(11)] = 1
    
    return hand

def hand_value(hand):
    return sum(hand)


 
# Seen Cards

def remove_seen(hand, cards):
    for card in hand:
        cards.pop(cards.index(card))



# Surviving

def survivablity(hand, deck):
    score = hand_value(hand)
    
    if score == 21:
        print("You have blackjack!")
        return
    
    # No Ace in hand
    if 11 not in hand:
        print("With a value of", score, "you need", 21 - score, "or less to not go bust")
        
        usable = 0
        current = 2
        
        usable += deck.count('A')
        
        while current <= (21 - score):
            if current == 10:
                usable += deck.count('10')
                usable += deck.count('J')
                usable += deck.count('Q')
                usable += deck.count('K')
                break
            else:
                usable += deck.count(str(current))
                current += 1
            
        
        print(usable)
        
        

    

print("Welcome to the Blackjack AI Advisor")
print("Please now enter your 2 cards (With pictures and Ace as a single letter): ")

player_hand = []

while len(player_hand) != 2:
    inputted = input(": ")
    if inputted in BASE_CARDS:
        player_hand.append(inputted)
    else:
        print("Invalid card")

remove_seen(player_hand, cards)    
player_hand = convert(player_hand)

print("So you are currently sitting on a value of", hand_value(player_hand))
survivablity(player_hand, cards)