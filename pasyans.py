#!/usr/bin/env python3

# Harrison Whitner 8/24/20

from enum import Enum, IntEnum  # for suits and ranks of cards
from random import shuffle  # for shuffling cards in a deck
from termcolor import colored  # for colored card text
from sys import exit  # for game quit


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


FACE_RANKS = [Rank.ACE, Rank.JACK, Rank.QUEEN, Rank.KING]

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
        if self.rank in FACE_RANKS:
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

    pasyans_cell_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'F', 'f']
    pasyans_move_commands = ['move', 'mv']
    pasyans_exit_commands = ['exit', 'end', 'quit']

    pasyans_win_count = 0

    # stacks which store info on previous moves
    pasyans_prev_move_src = None
    pasyans_prev_move_dst = None
    pasyans_prev_move_sz = None

    # main game loop, resets game after win achieved
    while True:

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

        # deal cards 4 cards in each of the 9 cells
        pasyans_cells = [[pasyans_deck.draw() for i in range(4)] for j in range(9)]

        # create free cell
        pasyans_free_cell = []

        # function for showing current game state
        def pasyans_show():

            # TODO clear terminal

            # iterate through row values, then through cells for printing
            for row in range(max([len(col) for col in pasyans_cells])):
                for col in pasyans_cells:
                    print(col[row].to_str() if row < len(col)
                          else '[  ]' if row == 0 and len(col) == 0 else '    ', '   ', end='')
                if row == 0:
                    print(pasyans_free_cell[0].to_str() if len(pasyans_free_cell) > 0 else '[  ]', sep='', end='')
                print()

            # print cell numbers and free cell at the bottom
            for i in range(9):
                print(' ' + str(i + 1) + '  ', '   ', end='')
            print(' F')

            # add blank line at bottom for spacing
            print()

        # function for checking if two cards are in a valid order
        def pasyans_valid(first, second) -> bool:

            # check if both cards are face or number
            if (first.rank in FACE_RANKS) != (second.rank in FACE_RANKS):
                return False

            # handle face cards
            elif first.rank in FACE_RANKS:
                return first.suit == second.suit

            # handle normal cards
            else:
                return first.diff_color(second) and first.rank == second.rank - 1

        # checks whether the current game state is a win
        def pasyans_check_win() -> bool:

            # check that every cell is in a valid order (empty is valid) and free cell is empty
            return all([all([pasyans_valid(col[-i], col[-i - 1]) for i in range(1, len(col))])
                        if len(col) > 0 else True for col in pasyans_cells]) and len(pasyans_free_cell) == 0

        # start game loop
        pasyans_win = False
        while not pasyans_win:

            # show cards
            pasyans_show()

            # loop until valid input is collected
            pasyans_command = None
            pasyans_args = None
            valid_input = False
            while not valid_input:

                # collect user input
                pasyans_input = input('> ').split()
                pasyans_command, pasyans_args = pasyans_input[0], pasyans_input[1:]

                # verify command
                if pasyans_command in pasyans_move_commands + ['win'] + pasyans_exit_commands:
                    valid_input = True

                else:
                    print('Invalid command. Valid commands: move <c> <c>, end, win')

            # handle move commands
            if pasyans_command in pasyans_move_commands:

                # check for invalid args
                if len(pasyans_args) < 2 or pasyans_args[0] not in pasyans_cell_names \
                        or pasyans_args[1] not in pasyans_cell_names:
                    print('Invalid move command. Valid form: move <c> <c>')

                else:
                    src_col = pasyans_free_cell if pasyans_args[0] in ['F', 'f'] \
                        else pasyans_cells[int(pasyans_args[0]) - 1]
                    dst_col = pasyans_free_cell if pasyans_args[1] in ['F', 'f'] \
                        else pasyans_cells[int(pasyans_args[1]) - 1]

                    # check for when source cell is empty
                    if len(src_col) == 0:
                        print('Source cell is empty, move cannot be performed.')

                    # check free cell not already filled
                    elif dst_col is pasyans_free_cell and len(pasyans_free_cell) > 0:
                        print('Free cell already contains a card, move cannot be performed.')

                    # otherwise, attempt the move
                    else:

                        # determine the max stack size (number of cards) that could be moved from src
                        stack_size = 1
                        if src_col is not pasyans_free_cell and len(src_col) > 1 and dst_col is not pasyans_free_cell:
                            while pasyans_valid(src_col[-stack_size], src_col[-stack_size - 1]):
                                stack_size += 1
                                if stack_size == len(src_col):
                                    break

                        # try to move max stack size to dst, then repeat with smaller sizes until successful or empty
                        while stack_size > 0:
                            # check if dst is empty first, always valid if so
                            if len(dst_col) == 0 or pasyans_valid(src_col[-stack_size], dst_col[-1]):
                                dst_col.extend(src_col[-stack_size:])  # copy stack from source to destination cell
                                del src_col[-stack_size:]  # remove stack from source cell
                                break
                            stack_size -= 1
                            
                        if stack_size == 0:
                            print('Invalid move.')

            # handle undo commands
            # elif pasyans_command == 'undo':
            # TODO implement undo command

            # handle win command
            elif pasyans_command == 'win':
                if pasyans_check_win():
                    pasyans_win = True
                    pasyans_win_count += 1
                    print('YOU WIN! Current win streak:', pasyans_win_count)
                    print('Creating new game...')
                else:
                    print('You have not won yet, sorry. Keep going!')

            # handle exit command
            elif pasyans_command in pasyans_exit_commands:
                if input('Are you sure you want to exit? ') in ['yes', 'y']:
                    exit()
