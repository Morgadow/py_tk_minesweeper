

class Size(object):

    def __init__(self, height, width):

        self.height = height
        self.width = width

    def __str__(self):
        return "Size | Width: {}, Height: {}".format(self.width, self.height)

    def __repr__(self):
        return '\n' + self.__str__() + '\n'


class Position:

    def __init__(self, x=None, y=None):

        self.x = x
        self.y = y

    def __str__(self):
        return "({}/{})".format(self.x, self.y)

    def __repr__(self):
        return '\n' + self.__str__() + '\n'


class GameSetting(object):

    def __init__(self, rows, cols, bombs):

        self.num_rows = rows
        self.num_cols = cols
        self.bombs = bombs  # amount of bombs
        # self.sound = False

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

