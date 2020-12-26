import utils



class Size(object):

    def __init__(self, height, width):

        self.height = height
        self.width = width

    def __str__(self):
        return "Size | Width: {}, Height: {}".format(self.width, self.height)

    def __repr__(self):
        return '\n' + self.__str__() + '\n'


class GameSetting(object):

    def __init__(self, rows, cols, bombs):

        self.num_rows = rows
        self.num_cols = cols
        self.bombs = bombs  # amount of bombs
        # self.sound = False

    # todo
    # def activate_sound(self):
    #     """
    #     activate game sound
    #     :return: None
    #     :rtype: None
    #     """
    #     self.sound = True
    #
    # def deactivate_sound(self):
    #     """
    #     deactivate game sound
    #     :return: None
    #     :rtype: None
    #     """
    #     self.sound = False


AVAILABLE_MODES = {  # todo different game settings: Beginner, Intermediate, ...
    'Beginner': GameSetting(rows=9, cols=9, bombs=10),
    'Intermediate': GameSetting(rows=16, cols=16, bombs=40),
    'Expert': GameSetting(rows=16, cols=30, bombs=99),
    'Custom': GameSetting(rows=None, cols=None, bombs=None)  # todo
}


class Game:
    """
    Basic Game status class for 'global' flags
    """
    def __init__(self, settings: GameSetting = AVAILABLE_MODES['Intermediate']):
        """

        :param settings:
        :type settings: GameSetting
        """
        self.logger = utils.get_logger(self.__class__.__name__)

        self.settings = settings
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
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __str__(self):
        return "({}/{})".format(self.x, self.y)

    def __repr__(self):
        return '\n' + self.__str__() + '\n'


