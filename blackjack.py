import random
import copy

DEBUG = 1

A = 'A'

# dealer wins everything on 21
# no hole card; no peak
# no surrender on A


class Deck(object):
    def __init__(self, deck_count):
        self.deck_count = deck_count
        self.cards = []
        for i in range(deck_count):
            for j in range(2,10):
                self.cards += [j] * 4
            self.cards += [10] * 16
            self.cards += [A] * 4

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop(0)


class Hand(object):
    def __init__(self, deck):
        self.cards = []
        self.deck = deck
        self.alternate_realities = {}

    def __len__(self):
        return len(self.cards)

    def draw(self):
        self.cards.append(self.deck.draw())

    @property
    def value(self):
        max_value = self._get_max_sub_22_value()
        if max_value is not None:
            return max_value
        return self._get_min_value()

    @property
    def is_soft(self):
        return len(self._get_sub_22_values()) > 1

    @property
    def is_hard(self):
        return not self.is_soft

    # ---player moves---

    DRAW = 'D'
    INSURE = 'I'
    SURRENDER = 'R'
    STAND = 'S'
    HIT = 'H'
    def play_multiple_realities(self, dealer_hand):
        if len(self.alternate_realities) == 0:
            assert len(self) == 2
            self._add_new_reality((Hand.DRAW,Hand.DRAW))
        while self.any_playable:
            next_card = self.deck.draw()
            for plays, hand in self.alternate_realities.items():
                if not Hand._is_playable(plays, hand):
                    continue
                self.surrender(plays, hand, dealer_hand),
                self.stand(plays, hand)
                self.hit(plays, hand, next_card)
                self.split(plays, hand)
                del self.alternate_realities[plays]

    @property
    def any_playable(self):
        return any([Hand._is_playable(plays, hand) for plays, hand in self.alternate_realities.items()])

    @classmethod
    def _is_playable(cls, plays, hand):
        not_playable = hand.value > 21 or plays[-1] in [Hand.SURRENDER, Hand.STAND]
        return not not_playable

    def _add_new_reality(self, plays, hand=None):
        if hand is None:
            hand = self
        self.alternate_realities[plays] = copy.deepcopy(hand)

    def surrender(self, plays, hand, dealer_hand):
        if len(dealer_hand) != 1 or dealer_hand.cards[0] == A or len(hand) != 2:
            return
        plays = plays + (Hand.SURRENDER,)
        self._add_new_reality(plays, hand)

    def stand(self, plays, hand):
        plays = plays + (Hand.STAND,)
        self._add_new_reality(plays, hand)

    def hit(self, plays, hand, next_card):
        plays = plays + (Hand.HIT,)
        hand.cards.append(next_card)
        self._add_new_reality(plays, hand)

    def split(self, plays, hand):
        pass

    # ---end player moves---

    def _get_min_value(self):
        return min(self._get_all_values())

    def _get_max_sub_22_value(self):
        sub_22 = self._get_sub_22_values()
        if sub_22:
            return max(sub_22)
        return None

    def _get_sub_22_values(self):
        sub_22 = [value for value in self._get_all_values() if value < 22]
        return sub_22

    def _get_all_values(self):
        values = [0]
        for card in self.cards:
            if card != A:
                values = [value + card for value in values]
            if card == A:
                values = [value + 1 for value in values] + [value + 11 for value in values]
        return list(set(values))


def dealer_play(hand):
    assert len(hand) == 1
    while hand.value < 17:
        if DEBUG: print 'Dealer hand (%s) with value of %s. Drawing...' % (hand.cards, hand.value)
        hand.draw()
    if hand.value > 21:
        if DEBUG: print 'Dealer **busted** with %s (%s)!' % (hand.value, hand.cards)
    else:
        if DEBUG: print 'Dealer stands with %s (%s)!' % (hand.value, hand.cards)

def player_play(player_hand, dealer_hand):
    assert len(player_hand) == 2
    assert len(dealer_hand) == 1
    player_hand.play_multiple_realities(dealer_hand)


#for i in range(100):
#    deck = Deck(6)
#    deck.shuffle()
#    h = Hand(deck)
#    for i in range(random.choice(range(1,6))):
#        h.draw()
#    if not h.is_soft:
#        continue
#    print 'Cards: %s' % h.cards
#    print 'Value: %s' % h.value
#    print 'Soft: %s' % h.is_soft
#    print 'Hard: %s' % h.is_hard
#    print


# Broken because the dealer gets cards at the end of the set
deck = Deck(6)
deck.shuffle()
dealer = Hand(deck)
player = Hand(deck)
player.draw()
dealer.draw()
player.draw()
player_play(player, dealer)
for plays, hand in player.alternate_realities.items():
    print '%s : %s (%s)'  % (plays, hand.value, hand.cards)
dealer_play(dealer)


