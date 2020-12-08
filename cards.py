#!/usr/bin/env python3

from enum import Enum, IntEnum  # For suits and ranks of cards
from random import shuffle  # For shuffling cards in a deck
from termcolor import colored  # For colored card text
import doctest  # For simple testing

""" CONSTANTS """


class Suit(Enum):
    SPADE = 1
    DIAMOND = 2
    CLUB = 3
    HEART = 4


class Rank(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


SUIT_TO_STR = {Suit.HEART: '♥',  # For converting suit enum to symbol
               Suit.DIAMOND: '♦',
               Suit.CLUB: '♣',
               Suit.SPADE: '♠'}

RANK_TO_STR = {Rank.ACE: 'A',  # For converting rank to string
               Rank.TWO: '2',
               Rank.THREE: '3',
               Rank.FOUR: '4',
               Rank.FIVE: '5',
               Rank.SIX: '6',
               Rank.SEVEN: '7',
               Rank.EIGHT: '8',
               Rank.NINE: '9',
               Rank.TEN: '10',
               Rank.JACK: 'J',
               Rank.QUEEN: 'Q',
               Rank.KING: 'K'}

""" CLASSES """


class Card:
    """Represents a single card in a french suited, standard 52 card deck."""

    rank = None
    suit = None

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def is_face(self) -> bool:
        return self.rank in [Rank.ACE, Rank.JACK, Rank.QUEEN, Rank.KING]

    def is_pip(self) -> bool:
        return self.rank not in [Rank.ACE, Rank.JACK, Rank.QUEEN, Rank.KING]

    def is_red(self) -> bool:
        return self.suit in [Suit.DIAMOND, Suit.HEART]

    def is_white(self) -> bool:
        return self.suit in [Suit.SPADE, Suit.CLUB]

    def get_color(self) -> str:
        return 'red' if self.is_red() else 'white'

    def is_same_color(self, other: 'Card') -> bool:
        return self.get_color() == other.get_color()

    def to_str(self) -> str:
        card_str = RANK_TO_STR[self.rank] + (' ' if self.rank == Rank.TEN else '  ') + SUIT_TO_STR[self.suit]

        if self.is_face():
            return colored(card_str, self.get_color(), attrs=['bold'])
        else:
            return colored(card_str, self.get_color())


class Deck:
    """Represents an entire french suited, standard 52 card deck."""

    cards = [Card(rank, suit) for suit in Suit for rank in Rank]  # 52 card deck unsorted default, top card is last

    def __init__(self, ranks='full'):
        if ranks == 'full':  # Full deck
            pass
        elif ranks == 'empty':  # Empty deck
            self.cards = []
        elif isinstance(ranks, list):  # List of desired ranks, ex. [SIX, SEVEN, EIGHT, KING]
            self.cards = [Card(rank, suit) for rank in ranks for suit in Suit]
        else:  # invalid arg
            self.cards = None
            raise ValueError  # TODO find better error type

    def shuffle(self):
        shuffle(self.cards)

    def show(self):
        for i in range(len(self.cards)):
            print(str(i) + ':', self.cards[i].to_str())

    def draw(self) -> Card:
        return None if len(self.cards) == 0 else self.cards.pop()

    def add(self, card: Card):
        self.cards.append(card)


class CardGameState:
    """Represents the history of a game, allowing turns to be reversed or a game to be resumed."""

    turn_history = []
    ready_to_exit = False
    is_won = False
    win_count = 0
    status_line = ''
    command = ''
    command_args = []

    def __init__(self, ranks, debug_mode=False):
        self.deck = Deck(ranks)
        self.debug_mode = debug_mode
