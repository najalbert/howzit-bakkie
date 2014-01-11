import random

DEBUG = 1

DECK_COUNT = 5
TRIALS = 100
HIT = 'H'
STAND = 'S'

def simulate_hands(player1, player2, dealer_up):
    DECK_BASE = [2,3,4,5,6,7,8,9,10,11]
    deck = DECK_BASE * 4 * DECK_COUNT 
    deck.remove(player1)
    deck.remove(player2)
    deck.remove(dealer_up)
    hit_hands = {}
    stand_bets = 0
    stand_wins = 0
    for i in range(TRIALS):
        random.shuffle(deck)
        next_card = 0
        strategy = random.choice([HIT, STAND])
        if strategy == HIT:
            hand = (player1, player2, deck[0])
            hit_hands.setdefault(hand, 0)
            hit_hands[hand] += 1
        elif strategy == STAND:
            stand_bets = 1
            stand_wins += score_hand(player1, player2, dealer_up, deck)
        else:
            raise Exception('Did you forget something?')

def score_hand(player1, player2, dealer_up, deck):
    if dealer_up + deck[0] == 21:
        wins = 0
        if DEBUG: print 'Player has %s ([%s, %s]) vs Dealer natural ([%s, %s]): win %s' % (score_player(player1, player2), player1, player2, dealer_up, deck[0], wins)
        return wins
    next_card_index = 1
    while score_dealer(dealer_up, next_card_index, deck) < 17:
        next_card_index += 1
    player_score = score_player(player1, player2)
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

    if DEBUG: print 'Player has %s ([%s, %s]) vs Dealer with %s (%s): win %s' % (player_score, player1, player2, dealer_score, [dealer_up] + deck[:next_card_index], wins)
    return wins

def score_player(player1, player2):
    if player1 == 11 and player2 == 11:
        return 12
    return player1 + player2

def score_dealer(dealer_up, end_of_dealer_hand, deck):
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



simulate_hands(7,8,6)

