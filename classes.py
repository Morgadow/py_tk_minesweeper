#!/usr/bin/python3.7
# -*- coding: utf-8 -*-


"""
utility classes for multipurpose usage
"""


import utils


class Size:
    """
    class for encapsulating size information with x and y axis size
    """

    def __init__(self, height, width):

        self.height = height
        self.width = width

    def __str__(self):
        return "Size | Width: {}, Height: {}".format(self.width, self.height)

    def __repr__(self):
        return '\n' + self.__str__() + '\n'


class GameSetting:
    """
    Class for encapsulating basic game settings size of game field and number of bombs
    """

    def __init__(self, rows, cols, bombs):

        self.num_rows = rows
        self.num_cols = cols
        self.bombs = bombs  # amount of bombs


class Game:
    """
    Basic Game status class for 'global' flags and game status evaluation
    """

    def __init__(self, possible_settings, chosen_setting):
        """
        constructor for setting up game settings based on game mode
        :param possible_settings: all possible settings stored in Minesweeper to select from
        :type possible_settings: dict
        :param chosen_setting: currently selected game mode
        :type chosen_setting: GameSetting
        """
        self.logger = utils.get_logger(self.__class__.__name__)

        self.possible_settings = possible_settings
        self.settings = chosen_setting
        self.running = False
        self.fields_left = None

    def start_game(self):
        """
        starts game and resets game fields left
        :return: None
        :rtype: None
        """
        self.fields_left = self.settings.num_rows * self.settings.num_cols - self.settings.bombs
        self.running = True

    def end_game(self):
        """
        stops game
        :return:
        :rtype:
        """
        self.running = False


class Position:
    """
    class for encapsulating a position with x and y axis data on game field
    """

    def __init__(self, x=None, y=None):
        """
        Position inside game field with x and y koordinates
        :param x: x-coordinate
        :type x: int
        :param y: y-coordinate
        :type y: int
        """

        self.x = x
        self.y = y

    def __eq__(self, other):
        """ Override of equals operator: is equal if x and y coordinates are matching """
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """ Override of not equals operator: is not equal if x or y coordinates are not matching """
        return self.x != other.x or self.y != other.y

    def __str__(self):
        return "({}/{})".format(self.x, self.y)

    def __repr__(self):
        return '\n' + self.__str__() + '\n'


