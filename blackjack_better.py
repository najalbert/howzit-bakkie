import random

DEBUG = 0

DECK_COUNT = 5
TRIALS = 10000
HIT = 'H'
STAND = 'S'

def simulate_hands(player_cards, dealer_up):
    DECK_BASE = [2,3,4,5,6,7,8,9,10,11]
    deck = DECK_BASE * 4 * DECK_COUNT 
    for card in player_cards:
        deck.remove(card)
    deck.remove(dealer_up)
    hit_hands = {}
    stand_bets = 0
    stand_wins = 0
    for i in range(TRIALS):
        random.shuffle(deck)
        next_card = 0
        strategy = random.choice([HIT, STAND])
        if strategy == HIT:
            hand = tuple(sorted(player_cards + (deck[0],)))
            hit_hands.setdefault(hand, 0)
            hit_hands[hand] += 1
        elif strategy == STAND:
            stand_bets += 1
            stand_wins += score_hand(player_cards, dealer_up, deck)
        else:
            raise Exception('Did you forget something?')
    print 'Expected value (over %s trials) of standing on %s %s with a dealer up card of %s and a 1 unit bet on the table is %s' % (TRIALS, score_cards(player_cards), player_cards, dealer_up, float(stand_wins)/stand_bets)

def score_hand(player_cards, dealer_up, deck):
    if dealer_up + deck[0] == 21:
        wins = 0
        if DEBUG: print 'Player has %s %s vs Dealer natural ([%s, %s]): win %s' % (score_cards(player_cards), player_cards, dealer_up, deck[0], wins)
        return wins
    next_card_index = 1
    while score_dealer(dealer_up, next_card_index, deck) < 17:
        next_card_index += 1
    player_score = score_cards(player_cards)
    dealer_score = score_dealer(dealer_up, next_card_index, deck)
    if player_score > dealer_score and player_score < 22:
        wins = 2
    if player_score > dealer_score and player_score >= 22:
        wins = 0
    elif player_score == dealer_score and player_score < 22:
        wins = 1
    elif player_score == dealer_score and player_score > 22:
        wins = 0
    elif player_score < dealer_score and player_score < 22 and dealer_score < 22:
        wins = 0
    elif player_score < dealer_score and player_score < 22 and dealer_score >= 22:
        wins = 2
    elif player_score < dealer_score and player_score >= 22 and dealer_score >= 22:
        wins = 0

    if DEBUG: print 'Player has %s %s vs Dealer with %s (%s): win %s' % (player_score, player_cards, dealer_score, [dealer_up] + deck[:next_card_index], wins)
    return wins

def score_dealer(dealer_up, end_of_dealer_hand, deck):
    return score_cards((dealer_up,) + tuple(deck[:end_of_dealer_hand]))
    total_score = dealer_up
    ace_count = 1 if dealer_up == 11 else 0
    for i in range(end_of_dealer_hand):
        card = deck[i]
        total_score += card
        if card == 11:
            ace_count  += 1
    for i in range(ace_count):
        if total_score > 22:
            total_score -= 10
    return total_score

def score_cards(cards):
    ace_count = 0
    total_score = 0
    for card in cards:
        if card == 11:
            ace_count += 1
        total_score += card
    for i in range(ace_count):
        if total_score > 21:
            total_score -= 10
    return total_score



simulate_hands((10,11,11,11,11,11,11,2),10)

