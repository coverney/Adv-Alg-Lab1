'''
This script tests the SET_solver to make sure that it finds valid sets from
a Hand. Here we assume that we have a standard SET deck with 81 cards.
Our properties are number of shapes, shape, shading, and color, which represent
indices in our Card values attribute.

For number of shapes: 1 -> 0, 2 -> 1, 3 -> 2
For shape: diamond -> 0, wave -> 1, oval -> 2
For shading: solid -> 0, striped -> 1, outline -> 2
For color: red -> 0, green -> 1, purple -> 2

A card with 1 red outlined wave would have a values attribute of
[0 (1 shape), 1 (wave), 2 (outline), 0 (red)]

In our tests, we pass in several triplets of cards into a Hand object and verify
the output of Hand's find_set() and find_set_brute_force() functions.

Run with pytest test.py
'''
import pytest
import random
import itertools
from SET_solver import Deck, Hand, Card

def is_valid_SET(SET):
    '''
    Given a set of Card objects determine whether they form a valid SET.
    Basically iterate through all properties, if there is any where the cards
    don't either all share a value or have different values then return False.
    '''
    for i in range(SET[0].p):
        values = [c.values[i] for c in SET]
        if len(set(values)) > 1 and len(set(values)) < len(values):
            return False
    return True

def test_valid_SET1():
    card1 = Card([0, 1, 2, 0]) # 1 red outlined wave
    card2 = Card([1, 2, 2, 1]) # 2 green outlined ovals
    card3 = Card([2, 0, 2, 2]) # 3 purple outlined diamonds
    hand = Hand([card1, card2, card3])
    set1 = hand.find_set() # returns a tuple
    assert is_valid_SET(set1) == True # should be a valid SET
    set2 = hand.find_set_brute_force() # returns a tuple
    assert is_valid_SET(set2) == True # should be a valid SET

def test_valid_SET2():
    card1 = Card([0, 0, 1, 1]) # 1 green striped diamond
    card2 = Card([1, 2, 2, 1]) # 2 green outlined ovals
    card3 = Card([2, 1, 0, 1]) # 3 green solid waves
    hand = Hand([card1, card2, card3])
    set1 = hand.find_set() # returns a tuple
    assert is_valid_SET(set1) == True # should be a valid SET
    set2 = hand.find_set_brute_force() # returns a tuple
    assert is_valid_SET(set2) == True # should be a valid SET

def test_invalid_SET1():
    card1 = Card([0, 0, 1, 0]) # 1 red striped diamond
    card2 = Card([0, 2, 2, 1]) # 1 green outlined ovals
    card3 = Card([0, 0, 0, 2]) # 1 purple solid diamond
    hand = Hand([card1, card2, card3])
    set1 = hand.find_set() # should return None
    assert set1 == None
    set2 = hand.find_set_brute_force() # should return None
    assert set2 == None
    assert is_valid_SET((card1, card2, card3)) == False # shouldn't be a valid SET

def test_invalid_SET2():
    # can't form a SET with only 2 cards
    card1 = Card([0, 0, 1, 0]) # 1 red striped diamond
    card2 = Card([0, 2, 2, 1]) # 1 green outlined ovals
    hand = Hand([card1, card2])
    set1 = hand.find_set() # should return None
    assert set1 == None
    set2 = hand.find_set_brute_force() # should return None
    assert set2 == None

def test_1000_valid_SETs():
    '''
    From a standard SET deck, generate 1000 hands and keep looking for SETs.
    If a SET is found, then make sure it is valid.
    '''
    deck = Deck()
    for i in range(1000):
        hand = deck.deal()
        set1 = hand.find_set()
        set2 = hand.find_set_brute_force()
        if set1 and set2:
            assert is_valid_SET(set1) == True
            assert is_valid_SET(set2) == True
        else:
            assert set1 == set2
