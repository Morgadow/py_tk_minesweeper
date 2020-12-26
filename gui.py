

import random
import tkinter as tk
import time

import utils
import field
import smiley
import counter
from classes import Size, Position, Game

from constants import *

"""
Timing Tests building game field (Tested with Intermediate Setting)

- Game field without fields and panels, but all borders, counters, smiley, ... : ~0.2s
- Load all images in classes: ~0.019s
- Creating Field and Panel objects WITHOUT labels and buttons : 0.00099s
- Building the 15x15 Buttons or Labels and placing : ~0.036s

Different building game field options:

1) Building fields and placing and building panels and placing them instantly in this order: t.time: 0.06 s (Looks a lot longer!)

2) Building fields without labels and building panels and placing panels instantly in this order: ~0.055 s  
"""


class MinesweeperGUI(object):

    # noinspection PyTypeChecker
    def __init__(self, game):

        self._root = None
        self.logger = utils.get_logger(self.__class__.__name__)

        # frames
        self._full_field = None
        self._upper_frame = None
        self._field_frame = None

        # game gui elements
        self._smiley: smiley.Smiley = None
        self._flag_counter: counter.FlagCounter = None
        self._timer_counter: counter.TimeCounter = None
        self._fields = []

        # basic game
        self._size: Size = None
        self.game: Game = game

        # images for game elements
        self._counter_images: counter.CounterImages = None
        self._smiley_images: smiley.SmileyImages = None
        self._field_front_images: field.FrontPanelImages = None
        self._field_back_images: field.BackPanelImages = None

    def build_gui(self):
        """
        main function to build main gui
        :return: None
        :rtype: None
        """
        # basic settings
        self._size = Size(
            width=self.game.settings.num_cols * (BACK_PANEL_WIDTH + LINE_BETWEEN_FIELDS) + RIGHT_FIELD_BORDER + LEFT_FIELD_BORDER + LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + RIGHT_GRAY_BORDER,
            height=self.game.settings.num_rows * (BACK_PANEL_WIDTH + LINE_BETWEEN_FIELDS) + FULL_HEIGHT_TOP_FRAME + BOT_GRAY_BORDER + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER + BOT_FIELD_BORDER + TOP_GRAY_BORDER + TOP_WHITE_BORDER
        )

        # icon and main field
        self._root = tk.Tk()
        self._root.title("Minesweeper")
        self._root.resizable(False, False)
        # tk.Canvas(self._root, bg=COLOR_LIGHT_GRAY, width=self._size.width-MULTIPLIER, height=self._size.height-MULTIPLIER).pack()  # todo rand abschneiden?  -> bug fixen unten und rechts weißer rand!
        tk.Canvas(self._root, bg=COLOR_LIGHT_GRAY, width=self._size.width, height=self._size.height).pack()
        self._root.wm_iconbitmap(bitmap=utils.resource_path("ui\\icon.ico"))
        self._root._size = self._size

        # images
        self._counter_images = counter.CounterImages()
        self._smiley_images = smiley.SmileyImages()
        self._field_front_images = field.FrontPanelImages()
        self._field_back_images = field.BackPanelImages()

        # # main borders
        top_white_border = tk.Label(self._root, bg=COLOR_WHITE).place(x=0, y=0, height=TOP_WHITE_BORDER, width=self._size.width)
        left_white_border = tk.Label(self._root, bg=COLOR_WHITE).place(x=0, y=0, height=self._size.height, width=LEFT_WHITE_BORDER)

        top_gray_border = tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=LEFT_WHITE_BORDER, y=TOP_WHITE_BORDER, width=self._size.width - LEFT_WHITE_BORDER, height=TOP_GRAY_BORDER)
        left_gray_border = tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=LEFT_WHITE_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER, width=LEFT_GRAY_BORDER, height=self._size.height - TOP_WHITE_BORDER - TOP_GRAY_BORDER)
        top_field_border = tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME, width=self._size.width - LEFT_GRAY_BORDER - LEFT_WHITE_BORDER - RIGHT_GRAY_BORDER, height=BORDER_TOP_FIELD_BORDER)
        right_gray_border = tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=self._size.width - RIGHT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER, width=RIGHT_GRAY_BORDER, height=self._size.height - TOP_GRAY_BORDER - TOP_WHITE_BORDER)
        bot_gray_border = tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=self._size.height - BOT_GRAY_BORDER, width=self._size.width - LEFT_GRAY_BORDER - LEFT_WHITE_BORDER - RIGHT_GRAY_BORDER, height=BOT_GRAY_BORDER)

        # upper area
        self._upper_frame = tk.Frame(self._root, bg=COLOR_LIGHT_GRAY)
        self._upper_frame._width = self.game.settings.num_cols * (BACK_PANEL_WIDTH + LINE_BETWEEN_FIELDS) + LEFT_FIELD_BORDER + RIGHT_FIELD_BORDER
        self._upper_frame._height = FULL_HEIGHT_TOP_FRAME
        self._upper_frame.place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER, width=self._upper_frame._width, height=self._upper_frame._height)

        # borders around upper area
        outer_border_top = tk.Label(self._upper_frame, bg=COLOR_MEDIUM_GRAY).place(x=0, y=0, width=self._upper_frame._width - OUTER_BORDER_TOP_FRAME, height=OUTER_BORDER_TOP_FRAME)
        outer_border_left = tk.Label(self._upper_frame, bg=COLOR_MEDIUM_GRAY).place(x=0, y=OUTER_BORDER_TOP_FRAME*2, width=OUTER_BORDER_TOP_FRAME, height=self._upper_frame._height - OUTER_BORDER_TOP_FRAME*3)
        outer_border_right = tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME, y=OUTER_BORDER_TOP_FRAME, width=OUTER_BORDER_TOP_FRAME, height=self._upper_frame._height - OUTER_BORDER_TOP_FRAME)
        outer_border_bottom = tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=OUTER_BORDER_TOP_FRAME, y=self._upper_frame._height-OUTER_BORDER_TOP_FRAME, width=self._upper_frame._width - OUTER_BORDER_TOP_FRAME*3, height=OUTER_BORDER_TOP_FRAME)

        inner_border_top = tk.Label(self._upper_frame, bg=COLOR_MEDIUM_GRAY).place(x=0, y=OUTER_BORDER_TOP_FRAME, width=self._upper_frame._width - OUTER_BORDER_TOP_FRAME*2, height=OUTER_BORDER_TOP_FRAME)
        inner_border_left = tk.Label(self._upper_frame, bg=COLOR_MEDIUM_GRAY).place(x=OUTER_BORDER_TOP_FRAME, y=OUTER_BORDER_TOP_FRAME*2, width=OUTER_BORDER_TOP_FRAME, height=self._upper_frame._height - OUTER_BORDER_TOP_FRAME*4)
        inner_border_right = tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME*2, y=OUTER_BORDER_TOP_FRAME*2, width=OUTER_BORDER_TOP_FRAME, height=self._upper_frame._height - OUTER_BORDER_TOP_FRAME*2)
        inner_border_bottom = tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=OUTER_BORDER_TOP_FRAME*2, y=self._upper_frame._height-OUTER_BORDER_TOP_FRAME*2, width=self._upper_frame._width - OUTER_BORDER_TOP_FRAME*4, height=OUTER_BORDER_TOP_FRAME)

        # flag counter area
        flag_counter_frame = tk.Frame(self._upper_frame)
        flag_counter_frame.place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER + BORDER_AROUND_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=COUNTER_WIDTH * 3, height=COUNTER_HEIGHT)
        top_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=COUNTER_WIDTH*3, height=BORDER_AROUND_COUNTER)
        left_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=BORDER_AROUND_COUNTER, height=COUNTER_HEIGHT+BORDER_AROUND_COUNTER)
        right_border = tk.Label(self._upper_frame, bg=COLOR_BOT_BORDER_COUNTER).place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER + COUNTER_WIDTH*3, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=BORDER_AROUND_COUNTER, height=COUNTER_HEIGHT + BORDER_AROUND_COUNTER)
        bottom_border = tk.Label(self._upper_frame, bg=COLOR_BOT_BORDER_COUNTER).place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER + BORDER_AROUND_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER + COUNTER_HEIGHT, width=COUNTER_WIDTH*3, height=BORDER_AROUND_COUNTER)
        self._flag_counter = counter.FlagCounter(flag_counter_frame, self.game.settings.bombs, self._counter_images, self.game)
        self._flag_counter.init()

        # timer counter area
        timer_counter_frame = tk.Frame(self._upper_frame)
        timer_counter_frame.place(x=self._upper_frame._width - COUNTER_WIDTH*3 - SPACER_RIGHT_COUNTER - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=COUNTER_WIDTH * 3, height=COUNTER_HEIGHT)
        top_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER*2 - COUNTER_WIDTH*3 - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=COUNTER_WIDTH*3 + BORDER_AROUND_COUNTER, height=BORDER_AROUND_COUNTER)
        left_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER*2 - COUNTER_WIDTH*3 - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=BORDER_AROUND_COUNTER, height=COUNTER_HEIGHT+BORDER_AROUND_COUNTER)
        right_border = tk.Label(self._upper_frame, bg=COLOR_BOT_BORDER_COUNTER).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=BORDER_AROUND_COUNTER, height=COUNTER_HEIGHT + BORDER_AROUND_COUNTER)
        bottom_border = tk.Label(self._upper_frame, bg=COLOR_BOT_BORDER_COUNTER).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER - COUNTER_WIDTH*3 - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER + COUNTER_HEIGHT, width=COUNTER_WIDTH*3 + BORDER_AROUND_COUNTER, height=BORDER_AROUND_COUNTER)
        self._timer_counter = counter.TimeCounter(timer_counter_frame, 0, self._counter_images, self.game)
        self._timer_counter.init()

        # smiley
        smiley_frame = tk.Frame(self._upper_frame)
        smiley_frame.place(x=(self._upper_frame._width - SMILEY_WIDTH) / 2, y=(FULL_HEIGHT_TOP_FRAME - SMILEY_HEIGHT) / 2, width=SMILEY_WIDTH, height=SMILEY_HEIGHT)
        top_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=(self._upper_frame._width - SMILEY_WIDTH) / 2 - SMILEY_BORDER, y=(FULL_HEIGHT_TOP_FRAME - SMILEY_HEIGHT) / 2 - SMILEY_BORDER, width=SMILEY_WIDTH + SMILEY_BORDER, height=SMILEY_BORDER)
        left_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=(self._upper_frame._width - SMILEY_WIDTH) / 2 - SMILEY_BORDER, y=(FULL_HEIGHT_TOP_FRAME - SMILEY_HEIGHT) / 2, width=SMILEY_BORDER, height=SMILEY_HEIGHT)
        right_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=(self._upper_frame._width - SMILEY_WIDTH) / 2 + SMILEY_WIDTH, y=(FULL_HEIGHT_TOP_FRAME - SMILEY_HEIGHT) / 2, width=SMILEY_BORDER, height=SMILEY_HEIGHT + SMILEY_BORDER)
        bot_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=(self._upper_frame._width - SMILEY_WIDTH) / 2, y=(FULL_HEIGHT_TOP_FRAME - SMILEY_HEIGHT) / 2 + SMILEY_HEIGHT, width=SMILEY_WIDTH + SMILEY_BORDER, height=SMILEY_BORDER)
        self._smiley = smiley.Smiley(smiley_frame, self._smiley_images, cb=self.new_game)
        self._smiley.init()

        # field area
        self._field_frame = tk.Frame(self._root, bg=COLOR_LINE_BETWEEN_FIELDS)
        self._field_frame._width = self.game.settings.num_cols * (BACK_PANEL_WIDTH + LINE_BETWEEN_FIELDS)
        self._field_frame._height = self.game.settings.num_rows * (BACK_PANEL_WIDTH + LINE_BETWEEN_FIELDS)
        self._field_frame.place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=self._field_frame._width, height=self._field_frame._height)

        top_1 = tk.Label(self._root, bg=COLOR_MEDIUM_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER, width=self._field_frame._width + LEFT_FIELD_BORDER + RIGHT_FIELD_BORDER_1 + RIGHT_FIELD_BORDER_2, height=TOP_FIELD_BORDER_1)
        top_2 = tk.Label(self._root, bg=COLOR_MEDIUM_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER_1, width=self._field_frame._width + LEFT_FIELD_BORDER + RIGHT_FIELD_BORDER_1, height=TOP_FIELD_BORDER_2)
        top_3 = tk.Label(self._root, bg=COLOR_MEDIUM_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER_1 + TOP_FIELD_BORDER_2, width=self._field_frame._width + LEFT_FIELD_BORDER, height=TOP_FIELD_BORDER_3)

        left_1 = tk.Label(self._root, bg=COLOR_MEDIUM_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=LEFT_FIELD_BORDER_1, height=self._field_frame._height + BOT_FIELD_BORDER_3 + BOT_FIELD_BORDER_2)
        left_2 = tk.Label(self._root, bg=COLOR_MEDIUM_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER_1, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=LEFT_FIELD_BORDER_2, height=self._field_frame._height + BOT_FIELD_BORDER_3)
        left_3 = tk.Label(self._root, bg=COLOR_MEDIUM_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER_1 + LEFT_FIELD_BORDER_2, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=LEFT_FIELD_BORDER_3, height=self._field_frame._height)

        right_1 = tk.Label(self._root, bg=COLOR_WHITE).place(x=self._root._size.width - RIGHT_GRAY_BORDER - RIGHT_FIELD_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=RIGHT_FIELD_BORDER_1, height=self._field_frame._height)
        right_2 = tk.Label(self._root, bg=COLOR_WHITE).place(x=self._root._size.width - RIGHT_GRAY_BORDER - RIGHT_FIELD_BORDER_3 - RIGHT_FIELD_BORDER_2, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER_1 + TOP_FIELD_BORDER_2, width=RIGHT_FIELD_BORDER_2, height=self._field_frame._height + TOP_FIELD_BORDER_1)
        right_3 = tk.Label(self._root, bg=COLOR_WHITE).place(x=self._root._size.width - RIGHT_GRAY_BORDER - RIGHT_FIELD_BORDER_3, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER_1, width=RIGHT_FIELD_BORDER_3, height=self._field_frame._height + TOP_FIELD_BORDER_1 + TOP_FIELD_BORDER_2)

        bot_1 = tk.Label(self._root, bg=COLOR_WHITE).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER, y=self._root._size.height - BOT_GRAY_BORDER - BOT_FIELD_BORDER, width=self._field_frame._width + + RIGHT_FIELD_BORDER, height=BOT_FIELD_BORDER_1)
        bot_2 = tk.Label(self._root, bg=COLOR_WHITE).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER_1 + LEFT_FIELD_BORDER_2, y=self._root._size.height - BOT_GRAY_BORDER - BOT_FIELD_BORDER_3 - BOT_FIELD_BORDER_2, width=self._field_frame._width + RIGHT_FIELD_BORDER + LEFT_FIELD_BORDER_3, height=BOT_FIELD_BORDER_2)
        bot_3 = tk.Label(self._root, bg=COLOR_WHITE).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER_1, y=self._root._size.height - BOT_GRAY_BORDER - BOT_FIELD_BORDER_3, width=self._field_frame._width + RIGHT_FIELD_BORDER + LEFT_FIELD_BORDER_3 + LEFT_FIELD_BORDER_2, height=BOT_FIELD_BORDER_3)

        # create fields and panels and prepare everything
        self.create_fields()
        self.new_game()

        self._root.mainloop()

    def create_fields(self, ):
        """
        initially create fields and panels and place them on the gamefield
        :return:
        :rtype:
        """
        # create fields
        for col in range(self.game.settings.num_cols):
            col_fields = []
            for row in range(self.game.settings.num_rows):

                elem = field.Field(Position(col, row), self.game, self._flag_counter.count_up, self._flag_counter.count_down, self._timer_counter.start_timer, self.reveal_emtpy_panels, self.game_won, self.game_lost)
                elem.add_back(self._field_frame, elem.pos, self._field_back_images)
                elem.add_front(self._field_frame, elem.pos, self._field_front_images)
                elem.back.place()
                elem.front.place()

                col_fields.append(elem)
            self._fields.append(col_fields)

        # todo play with idletasks as one way to improve compute time and generating gamefield to begin with
        # tk.update_idletasks()
        # tk.update()
        # # https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop

    def new_game(self):
        """
        start new game, resets field, sets new bombs and calculates all field numbers
        :return:
        :rtype:
        """
        self._reset_all_fields()
        self._smiley.set_start()
        self._give_out_bombs()
        self._update_all_fields(recalc=True)
        self._timer_counter.reset()
        self._flag_counter.reset(start=self.game.settings.bombs)
        self.game.running = True
        self.game.fields_left = self.game.settings.num_rows * self.game.settings.num_rows - self.game.settings.bombs

    def _give_out_bombs(self):
        """
        randomly select positions for bombs out of all possible positions
        :return: None
        :rtype: None
        """
        av_pos = []
        for x in range(self.game.settings.num_rows):
            for y in range(self.game.settings.num_cols):
                av_pos.append(Position(x, y))

        bombs = random.sample(av_pos, self.game.settings.bombs)
        for pos in bombs:
            self._fields[pos.x][pos.y].back.set_bomb()

    def _update_all_fields(self, recalc=False):
        """
        updates images on all back fields, can also calculate num bombs nearby for all fields
        :param recalc: if set all back field numbers are recalculated
        :type recalc: bool
        :return: None
        :rtype: None
        """
        t = time.time()
        if recalc:
            for x in range(self.game.settings.num_cols):
                for y in range(self.game.settings.num_rows):

                    sub_field = []
                    if x > 0:
                        sub_field.extend(self._fields[x-1][max(y-1, 0):min(y + 2, self.game.settings.num_rows)])
                    sub_field.extend(self._fields[x][max(y-1, 0):min(y + 2, self.game.settings.num_rows)])
                    if x < self.game.settings.num_cols-1:
                        sub_field.extend(self._fields[x+1][max(y-1, 0):min(y + 2, self.game.settings.num_rows)])

                    self._fields[x][y].back.bombs_near = [elem.back.has_bomb for elem in sub_field].count(True)
                    self._fields[x][y].back.update_img()

            utils.LOG.debug("calculating numbers took {}s".format(time.time() - t))

        else:  # no recalc
            for row in self._fields:
                for elem in row:
                    elem.back.update_img()

    def _reset_all_fields(self):
        """
        resets all fields for a new game with already built gui elements
        :return: None
        :rtype: None
        """
        for row in self._fields:
            for elem in row:
                elem.reset()

    def game_lost(self):
        """
        end game and run game lost routine
        :return:
        :rtype:
        """
        self.logger.info("Pressed on a bomb, game lost!")
        self.game.running = False
        self._smiley.set_lost()
        self._timer_counter.stop_timer()
        self.reveal_bombs()

    def game_won(self):
        """
        end game and run game lost routine
        :return:
        :rtype:
        """
        self.logger.info("All fields cleared, game won!")
        self.game.running = False
        self._smiley.set_won()
        self._timer_counter.stop_timer()
        self.reveal_bombs()
        # todo handle highscore

    def reveal_bombs(self):
        """
        unlaces front panels and reveals bombs behind
        :return: None
        :rtype: None
        """
        for x in range(self.game.settings.num_cols):
            for y in range(self.game.settings.num_rows):
                if self._fields[x][y].back.has_bomb and not self._fields[x][y].front.has_flag:
                    self._fields[x][y].revealed = True
                if self._fields[x][y].back.has_bomb and self._fields[x][y].front.has_flag:
                    self._fields[x][y].back.set_disarmed_bomb()
                    self._fields[x][y].revealed = True

    def reveal_emtpy_panels(self, pos):
        """
        reveals empty panels and all panels touching those
        :param pos: position of start panels which calls the method
        :type pos: Position
        :return: None
        :rtype: None
        """
        analyzed_panels = []
        empty_panels = [self._fields[pos.x][pos.y]]

        while len(empty_panels):
            elem = empty_panels.pop()
            analyzed_panels.append(elem)

            new_pans = self.__aux_ret_subfield(elem.pos)
            for elem in new_pans:
                if not elem.back.bombs_near and elem not in analyzed_panels:
                    empty_panels.append(elem)
                elem.revealed = True

    def __aux_ret_subfield(self, pos):
        """
        gathers all 8 subfields around position
        :param pos: position of middle field, wont be collected
        :type pos: Position
        :return: the 8 subfields around middle field
        :rtype: list
        """
        sub_field = []

        if pos.x > 0:
            sub_field.extend(self._fields[pos.x-1][max(pos.y-1, 0):min(pos.y + 2, self.game.settings.num_rows)])
        if pos.x < self.game.settings.num_cols-1:
            sub_field.extend(self._fields[pos.x+1][max(pos.y-1, 0):min(pos.y + 2, self.game.settings.num_rows)])
        if pos.y > 0:
            sub_field.append(self._fields[pos.x][pos.y-1])
        if pos.y < self.game.settings.num_rows-1:
            sub_field.append(self._fields[pos.x][pos.y+1])

        return sub_field
