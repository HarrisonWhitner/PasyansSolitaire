#!/usr/bin/env python3

# Harrison Whitner 8/24/20

from enum import Enum, IntEnum  # for suits and ranks of cards
from random import shuffle  # for shuffling cards in a deck
from termcolor import colored  # for colored card text


class Suit(Enum):
    SPADE = 1
    DIAMOND = 2
    CLUB = 3
    HEART = 4


RED_SUITS = [Suit.DIAMOND, Suit.HEART]
BLACK_SUITS = [Suit.SPADE, Suit.CLUB]


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


ROYAL_RANKS = [Rank.ACE, Rank.JACK, Rank.QUEEN, Rank.KING]

SUIT_TO_STR = {Suit.HEART: '♥',  # for converting suit enum to symbol
               Suit.DIAMOND: '♦',
               Suit.CLUB: '♣',
               Suit.SPADE: '♠'}

RANK_TO_STR = {Rank.ACE: 'A',  # for converting rank to string
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


class Card:
    rank = None
    suit = None

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    # for checking if this and another card have different colors
    def diff_color(self, other) -> bool:
        return (self.suit in RED_SUITS and other.suit in BLACK_SUITS) \
               or (self.suit in BLACK_SUITS and other.suit in RED_SUITS)

    def to_str(self) -> str:
        card_str = RANK_TO_STR[self.rank] + (' ' if self.rank == Rank.TEN else '  ') + SUIT_TO_STR[self.suit]
        if self.rank in ROYAL_RANKS:
            return colored(card_str, 'red' if self.suit == Suit.DIAMOND or self.suit == Suit.HEART else 'white',
                           attrs=['bold'])
        else:
            return colored(card_str, 'red' if self.suit == Suit.DIAMOND or self.suit == Suit.HEART else 'white')


class Deck:
    cards = [Card(rank, suit) for suit in Suit for rank in Rank]  # 52 card deck unsorted default, top card is last

    def __init__(self, cards='full'):
        if cards == 'full':  # full deck
            pass
        elif cards == 'empty':  # empty deck
            self.cards = []
        elif isinstance(cards, list):  # list of desired ranks, ex. [SIX, SEVEN, EIGHT, KING]
            self.cards = [Card(rank, suit) for rank in cards for suit in Suit]
        else:  # invalid arg
            self.cards = None
            raise ValueError  # TODO find better error type

    def shuffle(self):
        shuffle(self.cards)

    def show(self):
        for card in self.cards:
            print(card.to_str())

    def draw(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

    def add(self, card: Card):
        self.cards.append(card)


if __name__ == '__main__':  # main guard

    # create the pasyans deck
    # noinspection PyTypeChecker
    pasyans_deck = Deck([Rank.SIX,
                         Rank.SEVEN,
                         Rank.EIGHT,
                         Rank.NINE,
                         Rank.TEN,
                         Rank.JACK,
                         Rank.QUEEN,
                         Rank.KING,
                         Rank.ACE])

    # shuffle the deck
    pasyans_deck.shuffle()

    # deal cards into 9 columns of 4
    pasyans_columns = [[pasyans_deck.draw() for i in range(4)] for j in range(9)]

    # create column names
    pasyans_column_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'E']

    # create empty slot
    pasyans_empty = []

    # function for showing current game state
    def pasyans_show():

        # TODO clear terminal

        # iterate through row values, then through columns for printing
        for row in range(max([len(col) for col in pasyans_columns])):
            for col in pasyans_columns:
                print(col[row].to_str() if row < len(col)
                      else '[  ]' if row == 0 and len(col) == 0 else '    ', '   ', end='')
            if row == 0:
                print(pasyans_empty[0].to_str() if len(pasyans_empty) > 0 else '[  ]', sep='', end='')
            print()

        # print column numbers and empty at the bottom
        for i in range(9):
            print(' ' + str(i + 1) + '  ', '   ', end='')
        print(' E')

        # add empty line at bottom for spacing
        print()


    # function for checking if two cards are in a valid order
    def pasyans_valid(first, second) -> bool:

        # check both royal or normal
        if (first.rank in ROYAL_RANKS) != (second.rank in ROYAL_RANKS):
            return False

        # handle royal cards
        elif first.rank in ROYAL_RANKS:
            return first.suit == second.suit

        # handle normal cards
        else:
            return first.diff_color(second) and first.rank < second.rank


    # start game loop
    pasyans_win = False
    while not pasyans_win:

        # show cards
        pasyans_show()

        # loop until valid input is collected
        pasyans_input = None
        valid_input = False
        while not valid_input:

            # collect user input
            pasyans_input = input('> ').split()

            # verify input
            if pasyans_input[0] in ['move', 'mv', 'undo', 'end']:
                valid_input = True

            else:
                print('Invalid command. Valid commands: move <c> <c>, undo, end')

        # handle move commands
        if pasyans_input[0] in ['move', 'mv']:

            # check for invalid args
            if len(pasyans_input) < 3 or pasyans_input[1] not in pasyans_column_names \
                    or pasyans_input[2] not in pasyans_column_names:
                print('Invalid move command. Valid form: move <c> <c>')

            else:
                src_col = pasyans_empty if pasyans_input[1] == 'E' else pasyans_columns[int(pasyans_input[1]) - 1]
                dest_col = pasyans_empty if pasyans_input[2] == 'E' else pasyans_columns[int(pasyans_input[2]) - 1]

                # check for when source column is empty
                if len(src_col) == 0:
                    print('Source column is empty, move cannot be performed.')

                # check empty not already filled
                elif dest_col is pasyans_empty and len(pasyans_empty) > 0:
                    print('Empty already contains a card, move cannot be performed.')

                else:
                    block_size = 1  # determine how many cards will be moved in a block
                    if len(src_col) > 1 and src_col is not pasyans_empty and dest_col is not pasyans_empty:
                        while pasyans_valid(src_col[-block_size], src_col[-block_size - 1]):
                            block_size += 1
                            if block_size == len(src_col):
                                break

                    # check for invalid move
                    if len(dest_col) > 0 and not pasyans_valid(src_col[-block_size], dest_col[-1]):
                        while block_size > 0:  # try smaller block sizes if possible
                            block_size -= 1
                            if pasyans_valid(src_col[-block_size], dest_col[-1]):
                                dest_col.extend(src_col[-block_size:])  # copy block from source to destination column
                                del src_col[-block_size:]  # remove block from source column
                                break
                        if block_size == 0:
                            print('Invalid move.')

                    else:
                        dest_col.extend(src_col[-block_size:])  # copy block from source to destination column
                        del src_col[-block_size:]  # remove block from source column

        # handle undo commands
        # elif pasyans_input[0] == 'undo':

        # handle end commands TODO improve to check for win state or ask to leave
        elif pasyans_input[0] == 'end':
            pasyans_win = True
