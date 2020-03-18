'''
This script uses optimimum pair checking to find SETs in a hand of SET cards to solve the
3-Value SET problem. This approach uses partitioning methods to decrease the total
number of checks, resulting in an algorithm that is slightly better than
brute force.
'''
import random
import itertools
import timeit
from matplotlib import pyplot as plt
import numpy as np
from scipy import optimize
import time

class Deck:
    '''
    Deck represents our entire deck of SET cards! It is used to choose a random
    subset of cards for a Hand.
    '''
    def __init__(self, p=4, v=3):
        '''
        Create a deck given the number of properties and values by creating
        all possible cards and adding them to a list.
        '''
        self.cards = []
        self.p = p
        self.v = v
        self.size = self.v**self.p
        for i in range(self.size): # make each card
            values = []
            for j in range(self.p): # assign each property
                v_j = i % self.v
                values.append(v_j)
                i //= self.v
            c = Card(values)
            self.cards.append(c)

    def __repr__(self):
        '''
        Returns a string representing the deck. Since a deck necessarily
        contains all permutations of values for each property, it is not useful
        to print every card in the deck.
        '''
        return "Deck with %i cards, %i values, and %i properties" % (self.size, self.v, self.p)

    def deal(self, n=12):
        '''
        Pick n cards randomly from deck and pass it as a list to create a Hand.
        The default value for n is 12.
        '''
        # pick n cards from self.cards
        cards = random.sample(self.cards, n)
        return Hand(cards)

class Hand:
    '''
    Represents a subset of a Deck which has hypothetically been "dealt" so
    that SETs can be searched for among these cards.
    '''
    def __init__(self, cards):
        '''
        Takes a list of cards and creates a set of cards so that the presence of
        a card in the dealt cards can be checked in O(1) time.
        '''
        if cards is None:
            self.cards = set()
        else:
            self.cards = set(cards)
        self.size = len(self.cards)

    def __repr__(self):
        '''
        Returns a string representation of a Hand object.
        '''
        hand_str = 'Hand is: {\n'
        for card in self.cards:
            hand_str += str(card) + '\n'
        hand_str += '}'
        return hand_str

    def find_set(self):
        '''
        From the current hand, try to find a set using the optimum
        pair checking algorithm.

        The set of cards is split into two equal sized partitions and then
        pairs of cards are selected from both groups and calculate_third_card is called
        for each pair. From the calculated third cards, we call find_card to
        determine whether they are in the hand. If so, we found a set! If not,
        we keep generating pairs until we checked all of the cards.
        '''
        part1, part2 = list(self.cards)[:self.size//2], list(self.cards)[self.size//2:]
        pairs1 = list(itertools.combinations(part1, 2))
        pairs2 = list(itertools.combinations(part2, 2))
        pairs = pairs1 + pairs2
        for c1, c2 in pairs:
            c3 = self.calculate_third_card(c1, c2)
            if self.find_card(c3):
                return (c1, c2, c3)
        return None

    def find_set_brute_force(self):
        '''
        From the current hand, try to find a set using brute force.

        Pairs of cards are selected from the hand and calculate_third_card is called
        for each pair. From the calculated third cards, we call find_card to
        determine whether they are in the hand. If so, we found a set! If not,
        we keep generating pairs until we checked all of the cards.
        '''
        pairs = itertools.combinations(self.cards, 2)
        for c1, c2 in pairs:
            c3 = self.calculate_third_card(c1, c2)
            if self.find_card(c3):
                return (c1, c2, c3)
        return None

    def calculate_third_card(self, card1, card2):
        '''
        Given two SET cards, determine what the 3rd card needs to be to form a
        SET.
        '''
        # For each property, determine whether the two cards have the same or
        # distinct values
        card3_values = [0]*card1.p
        for p in range(card1.p):
            p_set = set([card1.values[p], card2.values[p]])
            # if the two cards share a property, the third card also needs to
            if len(p_set) < 2:
                card3_values[p] = card1.values[p]
            # if the two cards have distinct values, the third card needs to
            # the third distinct value
            else:
                # get the third distinct value
                card3_values[p] = list(set(range(card1.v)) - p_set)[0]
        return Card(card3_values)

    def find_card(self, card):
        '''
        Determine whether the inputted card is in the hand or not.
        Return True/False.
        '''
        return card in self.cards

class Card:
    '''
    Represents a SET card with a value for each property.
    '''
    def __init__(self, values):
        '''
        Creates a card object in which it has an attribute of values.
        Values is a list of values where index corresponds to the propery #
        '''
        self.p = len(values)
        self.v = 3 # our algorithm depends on the fact that v = 3
        self.values = values

    def __repr__(self):
        '''
        Returns a string representation of a Card object.
        '''
        card_str = 'Card: '
        for val in self.values:
            card_str += str(val) + ', '
        return card_str

    def __eq__(self, other):
        '''
        Overrides equals operator such that two cards are equal if and only if
        the values for each property are the same.
        '''
        for index, value in enumerate(self.values):
            if value != other.values[index]:
                return False
        return True

    def __hash__(self):
        '''
        Overrides hashing function for Card objects such that they can be added
        to a set.
        '''
        return hash(tuple(self.values))

def time_varying_n(n, deck, iters=1000):
    t = timeit.Timer('hand = deck.deal(n); hand.find_set()',
            globals=locals())
    return t.timeit(iters)

def time_varying_p(deck, iters=500):
    t = timeit.Timer('hand = deck.deal(); hand.find_set()',
            globals=locals())
    return t.timeit(iters)

def time_varying_n_bf(n, deck, iters=1000):
    t = timeit.Timer('hand = deck.deal(n); hand.find_set_brute_force()',
            globals=locals())
    return t.timeit(iters)

def time_varying_p_bf(deck, iters=500):
    t = timeit.Timer('hand = deck.deal(); hand.find_set_brute_force()',
            globals=locals())
    return t.timeit(iters)

def apply_params(x, a, b, c):
    return a * np.exp(-b * x) + c

if __name__ == '__main__':
    # TIMING: Time how long if takes to find sets for different values of n and p
    # Generate figures to compare brute force with optimum pair checking
    # xs = []
    # y1s = []
    # y2s = []
    # for i in range(8, 82):
    #     deck = Deck()
    #     xs.append(i)
    #     y1s.append(time_varying_n(i, deck))
    #     y2s.append(time_varying_n_bf(i, deck))
    #     print('Vary n:', i)
    #
    # z1 = np.polyfit(xs, y1s, 2)
    # z2 = np.polyfit(xs, y2s, 2)
    # p1 = np.poly1d(z1)
    # p2 = np.poly1d(z2)
    # plt.plot(xs, p1(xs), color='C0', linestyle=':')
    # plt.plot(xs, p2(xs), color='C1', linestyle=':')
    # plt.plot(xs, y1s, label='Optimum Pair Checking')
    # plt.plot(xs, y2s, label='Brute Force')
    # plt.rc('xtick',labelsize=20)
    # plt.rc('ytick',labelsize=20)
    # plt.xlabel('Number of cards dealt', fontsize=15, labelpad=10)
    # plt.ylabel('Time (s)', fontsize=15, labelpad=10)
    # plt.legend(fontsize=15)
    # plt.savefig("time_varying_n2.png", transparent=True, bbox_inches='tight')
    # plt.clf()

    start = time.time()
    xs = []
    y1s = []
    y2s = []
    for i in range(3, 16):
        deck = Deck(p=i)
        xs.append(i)
        y1s.append(time_varying_p(deck))
        y2s.append(time_varying_p_bf(deck))
        print('Vary p:', i)
    z1 = np.polyfit(xs, y1s, 2)
    z2 = np.polyfit(xs, y2s, 2)
    p1 = np.poly1d(z1)
    p2 = np.poly1d(z2)
    # z1opt, z1cov = optimize.curve_fit(lambda t,a,b,c: a*np.exp(b*t)+c,  xs,  y1s,  p0=(4, 0.1))
    # z2opt, z2cov = optimize.curve_fit(lambda t,a,b,c: a*np.exp(b*t)+c,  xs,  y2s,  p0=(4, 0.1))
    plt.plot(xs, p1(xs), color='C0', linestyle=':')
    plt.plot(xs, p2(xs), color='C1', linestyle=':')
    plt.plot(xs, y1s, label='Optimum Pair Checking')
    plt.plot(xs, y2s, label='Brute Force')
    plt.legend(fontsize=15)
    plt.rc('xtick',labelsize=20)
    plt.rc('ytick',labelsize=20)
    plt.xlabel('Number of properties', fontsize=15, labelpad=10)
    plt.ylabel('Time (s)', fontsize=15, labelpad=10)
    plt.savefig("time_varying_p3.png", transparent=True, bbox_inches='tight')

    end = time.time()
    print('Time elapsed:', end - start)

    # TESTING: create a deck and hand and then try to find a set in the hand
    # deck = Deck()
    # print(deck)
    # hand = deck.deal()
    # print(hand)
    # print(hand.find_set())

    # card_vals = input(">")
    # values = card_vals.split(' ')[:4]
    # c = Card([int(v) for v in values])
    # print(c)
    # print(hand.find_card(c))
