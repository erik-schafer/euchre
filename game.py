from card import Card
from deck import Deck
import random

class Game():
    def __init__(self, players):
        self.players = players
        self.score = [0, 0]
        self.rounds = []
        self.round = Round()

    def play(self):
        while not self.isdone:
            self.play_round()
    
    def play_round(self):
        self.round.play()
        winner = self.round.winner
        self.score[winner] += 1
        self.rounds.append(self.round)
        self.round = Round()

    @property
    def isdone(self):
        return max(self.score) >= 10

# class Round():
#     def __init__(self, players, dealer = 0):
#         self.deck: Deck = Deck(shuffled=False)
#         self.player_teams: dict[int, int] = {n: n%2 for n in range(4)}
#         self.tricks: list[int] = [0, 0]
#         self.makers: int | None = None
#         self.trump: int | None = None
#         self.stage: str = 'order_up'
#         self.actions: list[str] = [
#             'order_up',
#             'pass',
#             'make0',
#             'make1',
#             'make2',
#             'make3',
#             'pass_make',
#         ] + [
#             f'discard{c.id}' for c in self.deck.cards
#         ] + [
#             f'play{c.id}' for c in self.deck.cards
#         ]
#         self.deck.shuffle()        
#         self.dealer: int = dealer
#         self.eldest: int = (dealer + 1) % 4
#         self.players: list[Player] = players
#         self.player_act_id: int = self.eldest
#         self.hands: list[list[Card]] = [self.deck.deal(5) for p in players]
#         self.card_up: Card = self.deck.deal1()
    
#     def play(self):
#         # play the whole round till its done
#         pass

#     def step(self):
#         player_act = self.players[self.player_act_id]
#         if self.stage == 'order_up':
#             legal_actions = self.legal_actions(self.player_act_id)
#             action = player_act.choose_action(legal_actions)
#             self.process_order_up_action(action)

#         elif self.stage == 'dealer_discard':
#             legal_actions = self.legal_actions(self.player_act_id)
#             action = player_act.choose_action(legal_actions)
#             self.process_dealer_discard_action(action)
            
#         elif self.stage == 'make_trump':
#             pass
#         elif self.stage == 'play':
#             pass
    
#     def process_order_up_action(self, action):
#         if action == 'order_up':
#             dealer_hand = self.hands[self.dealer]
#             dealer_hand.append(self.card_up)
#             self.trump = self.card_up.suit
#             self.makers = self.player_teams[self.player_act_id]
#             self.stage = 'dealer_discard'
#             self.player_act_id = self.dealer
#             assert(len(self.hands[self.dealer]) == 6)
#         else:
#             if self.player_act_id == self.dealer:
#                 self.stage = 'make_trump'
#             self.next_player()
    
#     def process_dealer_discard_action(self, action):
#         discard_card_id = action.split('discard')[1]
#         discard_card_id = int(discard_card_id)        
#         dealer_hand = self.hands[self.dealer]
#         for i, card in enumerate(dealer_hand):
#             if card.id == discard_card_id:
#                 dealer_hand.pop(i)
#         self.hands[self.dealer] = dealer_hand
#         assert(len(self.hands[self.dealer]) == 5)

#     def process_make_trump_action(self, action):
#         if action == 'pass_make':
#             self.next_player()
#         else:
#             suit_id = action.split('make')[1]
#             suit_id = int(suit_id)
#             self.trump = suit_id
#             self.makers = self.player_teams[self.player_act_id]
#             self.next_player()

#     def legal_actions(self, player_id):
#         if self.stage == 'order_up':
#             return ['order_up', 'pass']
        
#         elif self.stage == 'dealer_discard':
#             assert(player_id == self.dealer and self.dealer == self.player_act_id) # sanity
#             dealer_hand = self.hands[self.dealer]
#             return [f'discard{c.id}' for c in dealer_hand]
        
#         elif self.stage == 'make_trump':
#             actions = [f'make{i}' for i in range(4)]
#             if self.player_act_id != self.dealer:
#                 actions += ['pass_make']
#             return actions
        
#         elif self.stage == 'play':
#             pass
    
#     def next_player(self):
#         self.player_act_id = (self.player_act_id + 1) % 4

#     @property
#     def tricks_played(self):
#         return sum(self.tricks)
    
#     @property
#     def isdone(self):
#         return self.tricks_played == 5

class Round():
    def __init__(self, players, dealer=0):
        self.deck: Deck = Deck(shuffled=False)
        self.player_teams: dict[int, int] = {n: n % 2 for n in range(4)}  # Team assignments
        self.tricks: list[int] = [0, 0]  # Trick count for each team
        self.makers: int | None = None  # Team that makes trump
        self.trump: int | None = None  # Trump suit
        self.stage: str = 'order_up'  # Stage of the round
        self.actions: list[str] = [
            'order_up', 'pass', 'make0', 'make1', 'make2', 'make3', 'pass_make',
        ] + [
            f'discard{c.id}' for c in self.deck.cards
        ] + [
            f'play{c.id}' for c in self.deck.cards
        ]
        self.deck.shuffle()        
        self.dealer: int = dealer
        self.eldest: int = (dealer + 1) % 4  # Player after dealer goes first
        self.players: list[Player] = players
        self.player_act_id: int = self.eldest  # Player who is taking action
        self.hands: list[list[Card]] = [self.deck.deal(5) for p in players]
        self.card_up: Card = self.deck.deal1()  # The card to be ordered up
        self.current_trick = []

    def play(self):
        """Play the whole round until it's done."""
        while not self.isdone:
            self.step()

    def step(self):
        player_act = self.players[self.player_act_id]
        legal_actions = self.legal_actions(self.player_act_id)
        action = player_act.choose_action(legal_actions)

        if self.stage == 'order_up':
            self.process_order_up_action(action)
        elif self.stage == 'dealer_discard':
            self.process_dealer_discard_action(action)
        elif self.stage == 'make_trump':
            self.process_make_trump_action(action)
        elif self.stage == 'play':
            self.process_play_action(action)

    def process_order_up_action(self, action):
        """Process the 'order up' or 'pass' actions."""
        if action == 'order_up':
            # Dealer picks up the card, setting the trump suit
            self.hands[self.dealer].append(self.card_up)
            self.trump = self.card_up.suit
            self.makers = self.player_teams[self.player_act_id]
            self.stage = 'dealer_discard'
            self.player_act_id = self.dealer  # Dealer discards after picking up
        else:
            if self.player_act_id == self.dealer:
                self.stage = 'make_trump'
            self.next_player()

    def process_dealer_discard_action(self, action):
        """Process the discard action for the dealer."""
        discard_card_id = int(action.split('discard')[1])
        dealer_hand = self.hands[self.dealer]
        self.hands[self.dealer] = [card for card in dealer_hand if card.id != discard_card_id]
        self.stage = 'play'
        self.player_act_id = self.eldest  # Eldest leads first

    def process_make_trump_action(self, action):
        """Process making trump or passing during the trump selection."""
        if action == 'pass_make':
            self.next_player()
        else:
            suit_id = int(action.split('make')[1])
            self.trump = suit_id
            self.makers = self.player_teams[self.player_act_id]
            self.stage = 'play'
            self.player_act_id = self.eldest

    def process_play_action(self, action):
        """Process a player's action during the play stage."""
        card_id = int(action.split('play')[1])
        player_hand = self.hands[self.player_act_id]
        card_played = next(card for card in player_hand if card.id == card_id)
        
        # Play the card and remove it from the player's hand
        player_hand.remove(card_played)
        self.current_trick.append((self.player_act_id, card_played))
        
        if len(self.current_trick) == 4:
            self.resolve_trick()

        self.next_player()

    def resolve_trick(self):
        """Resolve the winner of the current trick."""
        leading_suit = self.current_trick[0][1].suit
        winning_card = None
        winning_player = None

        # Find the winning card (considering trump)
        for player_id, card in self.current_trick:
            if winning_card is None or (
                card.suit == self.trump and winning_card.suit != self.trump) or (
                card.suit == winning_card.suit and card.val > winning_card.val):
                winning_card = card
                winning_player = player_id
        
        winning_team = self.player_teams[winning_player]
        self.tricks[winning_team] += 1
        self.current_trick = []
        self.player_act_id = winning_player  # Winner leads next trick

    def legal_actions(self, player_id):
        """Determine the legal actions available to the current player."""
        if self.stage == 'order_up':
            return ['order_up', 'pass']
        elif self.stage == 'dealer_discard':
            assert(player_id == self.dealer)  # Only the dealer can discard
            return [f'discard{c.id}' for c in self.hands[self.dealer]]
        elif self.stage == 'make_trump':
            actions = [f'make{i}' for i in range(4)]
            if self.player_act_id != self.dealer:
                actions += ['pass_make']
            return actions
        elif self.stage == 'play':
            # Must follow suit if possible, otherwise can play any card
            lead_suit = self.current_trick[0][1].suit if self.current_trick else None
            hand = self.hands[player_id]
            if lead_suit:
                valid_cards = [c for c in hand if c.suit == lead_suit]
                if not valid_cards:
                    valid_cards = hand  # No cards of lead suit; can play anything
            else:
                valid_cards = hand  # No lead yet; any card can be played
            return [f'play{c.id}' for c in valid_cards]

    def next_player(self):
        """Advance to the next player."""
        self.player_act_id = (self.player_act_id + 1) % 4

    @property
    def tricks_played(self):
        """Return the total number of tricks played."""
        return sum(self.tricks)

    @property
    def isdone(self):
        """Determine if the round is over (i.e., 5 tricks have been played)."""
        return self.tricks_played == 5


class Player():
    def __init__(self):
        pass

    def choose_action(self, legal_actions):
        return random.choice(legal_actions)