class Card():
    faces = {
        9: '9',
        10: '10',
        11: 'Jack',
        12: 'Queen',
        13: 'King',
        14: 'Ace'
    }
    suits = [
            'Spades',
            'Hearts',
            'Clubs',
            'Diamonds'
    ]
    def __init__(self, val: int, suit: int):
        self.val = val
        self.suit = suit

    @property
    def face(self):
        return self.faces[self.val]
    
    @property
    def suit_name(self):
        return self.suits[self.suit]
    
    @property 
    def color(self):
        return 'Black' if self.color_id == 0 else 'Red'

    @property
    def color_id(self):
        return self.suit % 2
    
    @property
    def id(self):
        return self.val + self.suit * 6
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f'{self.face} of {self.suit_name}'