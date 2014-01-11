import random

ODDS = 0
MIN_BET = 5
STARTING_STACK = 200
SIMULATION_ROUNDS = 10000
CHANCE_OF_FIELD_BET = 0
FIELD_BETS = [5]

DEBUG = 4

def roll():
    DICE = [1,2,3,4,5,6]
    return random.choice(DICE) + random.choice(DICE)

def play_round(pass_bet, odds_bet):
    if DEBUG > 5: print 'starting round:'
    if DEBUG > 5: print '\tbetting %s on pass' % pass_bet
    point = roll()
    field_cash = _play_the_field(point)
    if DEBUG > 5: print '\trolled %s' % point
    if point in [2, 3, 12]:
        if DEBUG > 5: print '\tcrapped out!'
        return odds_bet + field_cash
    if point in [7, 11]:
        if DEBUG > 5: print '\tpass wins!'
        return 2*pass_bet + odds_bet + field_cash
    if DEBUG > 5: print '\tlaying odds'
    while True:
        shoot = roll()
        field_cash += _play_the_field(point)
        if DEBUG > 5: print '\trolled a %s' % shoot
        if shoot == 7:
            if DEBUG > 5: print '\tcrapped out!'
            return 0 + field_cash
        if shoot == point:
            if DEBUG > 5: print '\tpass wins!'
            return 2*pass_bet + _odds_payout(odds_bet, point) + field_cash

def _play_the_field(roll):
    if random.random() > CHANCE_OF_FIELD_BET:
        return 0
    field_bet = random.choice(FIELD_BETS)
    # 2,3,4,9,10,11,12
    if roll == 2:
        if DEBUG > 5: print '\tplaced a $%s field bet and hit 2x on 2!' % field_bet
        return 2 * field_bet
    if roll == 12:
        if DEBUG > 5: print '\tplaced a $%s field bet and hit 3x on 12!' % field_bet
        return 3 * field_bet
    if roll in [3, 4, 9, 10, 11]:
        if DEBUG > 5: print '\tplaced a $%s field bet and hit %s!' % (field_bet, roll)
        return field_bet
    if DEBUG > 5: print '\tlost a $%s field bet!' % field_bet
    return -1 * field_bet


def _odds_payout(odds_bet, point):
    assert odds_bet % 5 == 0
    assert odds_bet % 2 == 0
    if point in [4, 10]:
        # Pay 2 to 1 
        return odds_bet + (2 * odds_bet)
    elif point in [5, 9]:
        # Pay 3 to 2
        return odds_bet + (3 * (odds_bet/2))
    elif point in [6, 8]:
        # Pay 6 to 5
        return odds_bet + (6 * (odds_bet/5))
    assert False, "unexpected point %s" % point

def play_with_stack(stack):
    rounds = 0
    odds_bet = ODDS * MIN_BET
    total_bet = MIN_BET + odds_bet
    max_stack = 0
    min_stack = stack
    wins = 0
    losses = 0
    while stack > total_bet:
        stack -= total_bet
        result = play_round(MIN_BET, ODDS*MIN_BET)
        stack += result
        if DEBUG > 4: print 'Won $%s, Stack is $%s' % (result, stack)
        max_stack = max_stack if stack < max_stack else stack
        min_stack = min_stack if stack > min_stack else stack
        if result >= total_bet:
            wins += 1
        else:
            losses += 1
        rounds += 1
    return rounds, max_stack, min_stack, wins, losses


def simulate_plays(play_count):
    results = []
    for i in range(play_count):
        rounds, max_stack, min_stack, wins, losses = play_with_stack(STARTING_STACK)
        print 
        if DEBUG > 3: print 'Played %s rounds with a stack of $%s (max: $%s, min: $%s, wins: %s, losses: %s)' % (rounds, STARTING_STACK, max_stack, min_stack, wins, losses)
        results.append((rounds, max_stack, min_stack, wins, losses))
    print
    print 'With a starting stack of %s, bet on pass of %s, and odds of %s, and %.02f%% chance of one of a %s field bets:' % (STARTING_STACK, MIN_BET, ODDS, CHANCE_OF_FIELD_BET*100, FIELD_BETS)
    print '\tAverage rounds played: %s' % (sum([result[0] for result in results])/len(results))
    print '\tMedian rounds played: %s' % sorted(results, key=lambda x: x[0])[len(results)/2][0]
    print
    print '\tAverage max stack: $%s' % (sum([result[1] for result in results])/len(results))
    print '\tMedian max stack: $%s' % sorted(results, key=lambda x: x[1])[len(results)/2][1] 
    print
    print '\tAverage wins: %s' % (sum([result[3] for result in results])/len(results))
    print '\tMedian wins: %s' % sorted(results, key=lambda x: x[3])[len(results)/2][3]
    print '\tAverage losses: %s' % (sum([result[4] for result in results])/len(results))
    print '\tMedian losses: %s' % sorted(results, key=lambda x: x[4])[len(results)/2][4]
    print
    print '\tPercentage plays where max stack is greater than starting stack: %.01f%%' % ((float(sum([1 for result in results if result[1] > STARTING_STACK]))/len(results)) * 100)

def main():
    simulate_plays(SIMULATION_ROUNDS)

if __name__ == "__main__":
    main()

