from collections import defaultdict

s1 = 0
s2 = 0

RANKS = dict((str(i),i) for i in range(2,10))
RANKS[u'T'] = 10
RANKS[u'J'] = 11
RANKS[u'Q'] = 12
RANKS[u'K'] = 13
RANKS[u'A'] = 14

def rank_card(card):
    """determine rank of a card."""
    return RANKS[card[0]]


def top_card(hand):
    return max(map(rank_card, hand))


def high_card(hand):
    return top_card(hand)


def one_pair(hand):
    return n_of_a_kind(hand, 2)


def two_pairs(hand):
    cards = defaultdict(int)
    for c in hand:
        cards[c[0]] += 1
    pairs = 0
    for count in cards.itervalues():
        if count == 2:
            pairs += 1
    return 1 if pairs == 2 else 0


def three_of_a_kind(hand):
    return n_of_a_kind(hand, 3)


def n_of_a_kind(hand, n):
    cards = defaultdict(int)
    for c in hand:
        cards[c[0]] += 1
    for count in cards.itervalues():
        if count == n:
            return 1
    return 0

def straight(hand):
    # TODO: mike's rule
    bottom = 14
    top = 2
    for c in hand:
        rank = rank_card(c)
        if rank > top:
            top = rank
        if rank < bottom:
            bottom = rank
    
    return 1 if top - bottom == 4 else 0


def flush(hand):
    suit = hand[0][1]
    for c in hand[1:]:
        if suit != c[1]:
            return 0
    return 1


def full_house(hand):
    three = three_of_a_kind(hand)
    pair = one_pair(hand)
    return three and pair
    return 1 if three == 1 and pair == 1 else 0


def four_of_a_kind(hand):
    return n_of_a_kind(hand, 4)


def straight_flush(hand):
    return 1 if straight(hand) and flush(hand) else 0


def royal_flush(hand):
    sf = straight_flush(hand)
    if sf == 1 and top_card(hand) == 14:
        return 1
    return 0


HAND_SCORES = [
    (10, royal_flush),
    (9, straight_flush)
]

def score(hand):
    for (s,func) in HAND_SCORES:
        if func(hand):
            return s


with open('poker_file.txt', u'r') as infile:
    for line in infile:
        cards = line.split(u' ')
        hand1 = cards[:5]
        hand2 = cards[5:]
        score1 = score(hand1)
        score2 = score(hand2)
        
        if score1 == score2:
            top1 = top_card(hand1)
            top2 = top_card(hand2)
            if top1 < top2:
                s2+=1
            else:
                s1+=1

print u'player 1 wins %d hands' % s1

