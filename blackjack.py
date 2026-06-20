# Card Setup

BASE_CARDS = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']

def deck(decks):
    cards = decks * 4 * BASE_CARDS
    return cards

decks = 1
cards = deck(decks)


# Scoring

SCORING = {
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 11  # If score goes over 21 but contains 11, you can remove 10 from the scoring for A = 1
}

def convert(hand):
    for card in range(len(hand)):
        hand[card] = SCORING[hand[card]]
    
    return hand
