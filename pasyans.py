#!/usr/bin/env python3

from cards import Card, Deck, Rank, CardGameState
import os  # for clearing shell

"""
TITLE: Pasyans (пасьянс in Russian, "patience" in English)
DESCRIPTION: A simple to play, easy to install solitaire-esque game played in a terminal
AUTHOR: Harrison Whitner
START DATE: 8/24/20
"""


class PasyansGameState(CardGameState):
    """Represents the history of a Pasyans game, allowing turns to be reversed or a game to be resumed."""

    ranks = [Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE]
    command_aliases = {'move': ['move', 'mv'],
                       'exit': ['exit', 'end', 'quit'],
                       'win': ['win']}
    cell_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'F', 'f']

    def __init__(self):
        super().__init__(self.ranks)
        self.deck.shuffle()
        self.cells = [[self.deck.draw() for i in range(4)] for j in range(9)]
        self.free_cell = None

    def reset_game(self):
        self.deck = Deck(self.ranks)
        self.deck.shuffle()
        self.cells = [[self.deck.draw() for i in range(4)] for j in range(9)]
        self.free_cell = None

        self.turn_history = []
        self.is_won = False


def pasyans_show(gs: PasyansGameState):
    """Displays the current game state."""

    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print status line
    print('═> ' + gs.status_line + ' <' + '═' * (71 - len(gs.status_line))
          if len(gs.status_line) > 0 else '═' * 76)

    # Iterate through row values, then through cells for printing
    for row in range(max([len(cell) for cell in gs.cells])):
        for cell in gs.cells:
            print(cell[row].to_str() if row < len(cell)
                  else '[  ]' if row == 0 and len(cell) == 0 else '    ', '   ', end='')
        if row == 0:
            print(gs.free_cell.to_str() if gs.free_cell else '[  ]', sep='', end='')
        print()

    # Add blank line between cells and cell numbers
    print()

    # Print cell numbers and free cell at the bottom
    for i in range(9):
        print(' ' + str(i + 1) + '  ', '   ', end='')
    print(' F')

    # Add blank line at bottom for spacing
    print()


def pasyans_valid_order(first: Card, second: Card) -> bool:
    """Checks if two cards are in a valid order for Pasyans."""

    # Check if both cards are face or pip
    if first.is_face() != second.is_face():
        return False

    # Handle face cards
    elif first.is_face():
        return first.suit == second.suit

    # Handle pip cards
    else:
        return not first.is_same_color(second) and first.rank == second.rank - 1


def pasyans_check_win(gs: PasyansGameState) -> bool:
    """Checks whether the current game state is a win."""

    # Check that every cell is in a valid order (empty is valid) and free cell is empty
    return all([all([pasyans_valid_order(cell[-i], cell[-i - 1]) for i in range(1, len(cell))])
                if len(cell) > 0 else True for cell in gs.cells]) and not gs.free_cell


def pasyans_get_user_command(gs: PasyansGameState):
    """Collects command details from user input."""

    # Collect user input
    pasyans_input = input('» ').split()
    user_command = '' if len(pasyans_input) == 0 else pasyans_input[0]
    user_args = [] if len(pasyans_input) == 0 else pasyans_input[1:]

    # Clear previous turn's command details
    gs.command = ''
    gs.command_args = []

    for cmd in gs.command_aliases.keys():
        if user_command in gs.command_aliases[cmd]:
            gs.command = cmd
            gs.command_args = user_args
            break

    if gs.command == '':
        gs.status_line = 'invalid command, try `help`'


def pasyans_move_command(gs: PasyansGameState):
    """Moves a card from one cell to another."""

    # Check for invalid args
    if len(gs.command_args) < 2 or gs.command_args[0] not in gs.cell_names or gs.command_args[1] not in gs.cell_names:
        gs.status_line = 'invalid move arguments, try `move <c> <c>`'

    else:
        src_cell = gs.free_cell if gs.command_args[0] in ['F', 'f'] else gs.cells[int(gs.command_args[0]) - 1]
        dst_cell = gs.free_cell if gs.command_args[1] in ['F', 'f'] else gs.cells[int(gs.command_args[1]) - 1]

        # Check for when source cell is empty
        if len(src_cell) == 0:
            gs.status_line = 'source cell is empty, move cannot be performed'

        # Check if free cell not already filled
        elif dst_cell is gs.free_cell and gs.free_cell:
            gs.status_line = 'free cell already contains a card, move cannot be performed'

        # Otherwise, attempt the move
        else:
            # Determine the max stack size (number of cards) that could be moved from src
            stack_size = 1
            if src_cell is not gs.free_cell and len(src_cell) > 1 and dst_cell is not gs.free_cell:
                while pasyans_valid_order(src_cell[-stack_size], src_cell[-stack_size - 1]):
                    stack_size += 1
                    if stack_size == len(src_cell):
                        break

            # Try to move max stack size to dst, then repeat with smaller sizes until successful or empty
            while stack_size > 0:
                # Check if dst is empty first, always valid if so
                if len(dst_cell) == 0 or pasyans_valid_order(src_cell[-stack_size], dst_cell[-1]):
                    dst_cell.extend(src_cell[-stack_size:])  # Copy stack from source to destination cell
                    del src_cell[-stack_size:]  # Remove stack from source cell
                    gs.status_line = ''
                    gs.turn_history.append((src_cell, dst_cell, stack_size))
                    break
                stack_size -= 1

            if stack_size == 0:
                gs.status_line = 'invalid move'


def pasyans_win_command(gs: PasyansGameState):
    """Checks if the current 'game' is won, resets it if so."""

    if pasyans_check_win(gs):
        gs.is_won = True
        gs.win_count += 1
        gs.status_line = 'YOU WIN! current win streak: ' + str(gs.win_count)

    else:
        gs.status_line = "you haven't won yet, keep going!"


def pasyans_exit_command(gs: PasyansGameState):
    """Exits the session cleanly."""

    if input('are you sure you want to exit? » ') in ['yes', 'y']:
        gs.is_won = True
        gs.ready_to_exit = True


def pasyans_help_command(gs: PasyansGameState):
    """Displays a help message about commands."""
    pass  # TODO implement help command


def pasyans_rules_command(gs: PasyansGameState):
    """Displays a message which outlines the rules of Pasyans."""
    pass  # TODO implement rules command


def pasyans_undo_command(gs: PasyansGameState):
    """Undoes the previous move."""
    pass  # TODO implement undo command


def pasyans_solve_command(gs: PasyansGameState):
    """Tries to automatically solve the current 'game', displaying the necessary moves if possible, then resetting."""
    pass  # TODO implement solve command


def pasyans_main():
    """Starts the the game.
    The game operates through 2 loops: the session loop and the game loop.
    The session loop represents the current Pasyans session and iterates through 'games' of Pasyans.
    The game loop represents the current 'game' of Pasyans and iterates through turns of the 'game'.
    """

    # Create the game state
    pasyans_gs = PasyansGameState()

    # Session loop, resets game after win achieved
    while not pasyans_gs.ready_to_exit:

        # 'Game' loop, reads and applies commands
        while not pasyans_gs.is_won:

            # Show cards
            pasyans_show(pasyans_gs)

            # Collect user input to determine the command
            pasyans_get_user_command(pasyans_gs)

            if pasyans_gs.command == 'move':
                pasyans_move_command(pasyans_gs)

            elif pasyans_gs.command == 'win':
                pasyans_win_command(pasyans_gs)

            elif pasyans_gs.command == 'exit':
                pasyans_exit_command(pasyans_gs)

        if not pasyans_gs.ready_to_exit:
            pasyans_gs.is_won = False
            pasyans_gs.reset_game()


if __name__ == '__main__':  # Main guard
    pasyans_main()
