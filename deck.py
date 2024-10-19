import random
from card import Card

class Deck():
    def __init__(self, shuffled=True):
        values = [9, 10, 11, 12, 13, 14]
        suits = [0, 1, 2, 3]
        self.cards = []
        self.ptr = 0
        for v in values:
            for s in suits:
                self.cards.append(Card(v, s))
        if shuffled:
            self.shuffle()        
    
    def shuffle(self):
        self.ptr = 0
        random.shuffle(self.cards)

    def deal1(self):
        if self.ptr >= len(self.cards):
            return None
        c = self.cards[self.ptr]
        self.ptr += 1
        return c
    
    def deal(self, n: int):
        return [self.deal1() for _ in range(n)]
    
    def __len__(self):
        return len(self.cards)