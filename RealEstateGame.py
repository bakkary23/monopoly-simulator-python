"""
Author: Bashar Akkary
GitHub username: bakkary23
Date: 5/23/22
Description: This program simulates a simplified version of the game monopoly. It creates a game
object whose methods can be called to play the game. Players roll one die and loop around a game board
of 25 spaces. Spaces can be purchased and then if landed on by a non-owner player will charge rent.
A player loses if their account balance reaches zero. The last player with a nonzero bank account is
the winner.
"""


import random


class RealEstateGame:

    def __init__(self):
        self._game_board = {}
        self._player_list = {}

    def create_spaces(self, go_money, rent_amounts):
        """
        Takes as parameters the money awarded by the starting 'GO' square and an array containing
        24 rent prices and initializes the game board as a dictionary of space dictionary
        objects with keys for owner, rent, and price. Rent prices are randomized across the 24
        spaces. Returns false if number of rents in list is not 24
        """
        if len(rent_amounts) != 24:
            return False
        _space_amount = 0
        self._game_board = {}
        while _space_amount < 25:
            if _space_amount == 0:
                _space_info = {'Award': go_money}
                self._game_board['GO'] = _space_info
            else:
                _new_space = _space_amount
                _space_rent = _space_amount - 1
                _space_info = {'Owner': '', 'Rent': rent_amounts[_space_rent], 'Price': rent_amounts[_space_rent]*5}
                self._game_board[_new_space] = _space_info
            _space_amount += 1
        return self._game_board

    def create_player(self, name, init_bal):
        """
        Creates new player dictionary object, adds it to player list dictionary.
        Player dictionary object contains total balance and current position of player
        """
        _new_player = {'Balance': init_bal, 'Position': 0}
        self._player_list[name] = _new_player

    def get_player_list(self):
        """
        Returns dictionary of players
        """
        return self._player_list

    def get_game_board(self):
        """
        Returns game board dictionary object
        """
        return self._game_board

    @staticmethod
    def die_roll():
        """
        Simulates a die roll by returning a random value in the range [1, 6]
        """
        _roll = random.randrange(1, 7)
        return _roll

    def get_player_account_balance(self, name):
        """
        Takes player name string as parameter and returns account balance
        """
        _player = self._player_list[name]
        return _player['Balance']

    def get_player_current_position(self, name):
        """
        Takes player name string as parameter and returns current position
        """
        _player = self._player_list[name]
        return _player['Position']

    def get_space_cost(self, position):
        """
        Takes integer representing current position and returns cost of space
        """
        _space = self._game_board[position]
        return _space['Price']

    def get_space_rent(self, position):
        """
        Takes integer representing current position and returns rent of space
        """
        _space = self._game_board[position]
        return _space['Rent']

    def get_current_owner(self, position):
        """
        Takes integer representing current position and returns owner of space object
        """
        _space = self._game_board[position]
        return _space['Owner']

    def buy_space(self, name):
        """
        Takes as a parameter string representing player name and buys space for that player.
        Returns false if current position is the 'GO' space, space already has an owner, and
        player's current balance exceeds the cost of the space. Returns true if conditions for
        purchase are correct.
        """
        _current_pos = self.get_player_current_position(name)
        _current_space = self._game_board[_current_pos]
        _space_cost = self.get_space_cost(_current_pos)
        _current_balance = self.get_player_account_balance(name)
        _current_owner = self.get_current_owner(_current_pos)
        _current_player = self._player_list[name]
        if _current_balance > _space_cost and _current_owner == '' and _current_pos != 0:
            _current_player['Balance'] = _current_balance - _space_cost
            _current_space['Owner'] = name
            return True
        else:
            return False

    def player_loss(self, name):
        """Takes as a parameter string of player's name and removes the player's name
        from the 'Owner' key of any space objects they own if they in the event of a loss
        """
        _pos = 1
        while _pos < 25:
            if self.get_current_owner(_pos) == name:
                _space = self._game_board[_pos]
                _space['Owner'] = ''
            _pos += 1

    def move_player(self, name, move):
        """
        Takes as parameters a string of a player's name and the number of spaces to move. Verifies if
        move is legal and returns False if not.
        If the player lands on of passes the 'GO' spot, they are awarded money according to game board's
        initialization. If player lands on a space owned by another player, they will pay rent to
        the owner or the equivalent of their entire account balance if they don't have enough money.
        If the player's account balance is emptied in this turn, the player_loss method is called.
        If the space does not have an owner, the function returns.
        """
        if move < 1 or move > 6:
            return False
        if self.get_player_account_balance(name) == 0:
            return False
        _new_spot = self.get_player_current_position(name) + move
        _current_player = self._player_list[name]
        if _new_spot >= 25:
            _new_spot -= 25
            _go_spot = self._game_board['GO']
            _current_player['Balance'] += _go_spot['Award']
        _current_player['Position'] = _new_spot
        if _new_spot == 0:
            return
        if self.get_current_owner(_new_spot) != '':
            _rent = self.get_space_rent(_new_spot)
            _owner = self.get_current_owner(_new_spot)
            _current_owner = self._player_list[_owner]
            if self.get_player_account_balance(name) - _rent < 0:
                _current_owner['Balance'] += _current_player['Balance']
                _current_player['Balance'] = 0
            else:
                _current_owner['Balance'] += _rent
                _current_player['Balance'] -= _rent
        else:
            return
        if _current_player['Balance'] == 0:
            self.player_loss(name)
        return

    def check_game_over(self):
        """
        Checks whether the game is over, i.e. every player except for one has an account balance
        of zero. Returns the victor's name if the game is over and an empty string otherwise.
        """
        _check = 0
        _victor = ''
        for element in self._player_list:
            if self.get_player_account_balance(element) != 0:
                _check += 1
                _victor = element
        if _check == 1:
            return _victor
        else:
            return ''

"""Tests"""
# game = RealEstateGame()
#
# rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150,
#          150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350, 350, 350]
# game.create_spaces(50, rents)
#
# game.create_player("Player 1", 3000)
# game.create_player("Player 2", 1000)
# game.create_player("Player 3", 0)
#
# print(game.get_game_board())
# game.move_player('Player 1', 6)
# print("Player 1 first position:", game.get_player_current_position('Player 1'))
# print("Player 1 initial balance:", game.get_player_account_balance('Player 1'))
# print("Space 6 cost:", game.get_space_cost(6))
# print("Space 6 rent:", game.get_space_rent(6))
# game.buy_space('Player 1')
# print(game.get_game_board())
# print(game.get_player_list())
# game.move_player('Player 2', 6)
# print(game.buy_space('Player 2'))
# print(game.get_player_list())
# game.move_player('Player 3', 6)
# game.move_player('Player 2', 4)
# game.buy_space('Player 2')
# print(game.get_player_list())
# print(game.check_game_over())
