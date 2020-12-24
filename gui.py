

import random
import threading
import tkinter as tk
import time

import utils
import minesweeper as mw
import field
import panel
import smiley
import counter
from classes import Size, GameSetting, Position

from constants import *

"""
Timing Tests building gamefield (Tested with Intermidiate Setting)

- Gamefield without fields and panels, but all borders, counters, smiley, ... : ~0.2s
- Load all images in classes: ~0.019s
- Creating Field and Panel objects WITHOUT labels and buttons : 0.00099s
- Building the 15x15 Buttons or Labels and placing : ~0.036s

Different building game field options:

1) Building fields and placing and building panels and placing them instantly in this order: t.time: 0.06 s (Looks a lot longer!)

2) Building fields without labels and building panels and placing panels instantly in this order: ~0.055 s  
"""


class MinesweeperGUI(object):

    def __init__(self):

        self._root = None

        self._full_field = None
        self._upper_frame = None
        self._field_frame = None

        self._smiley = None
        self._flag_counter = None
        self._timer_counter = None
        self._fields = []

        self.setting = None
        self._size = None

        self._counter_images = None
        self._smiley_images = None
        self._field_images = None
        self._panel_images = None

    def build_gui(self, game_setting: GameSetting = mw.AVAILABLE_MODES['Intermediate']):
        """
        main function to build main gui
        :return: None
        :rtype: None
        """
        # basic settings
        self.setting = game_setting
        self._size = Size(
            width=game_setting.num_cols * (FIELD_WIDTH + LINE_BETWEEN_FIELDS) + RIGHT_FIELD_BORDER + LEFT_FIELD_BORDER + LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + RIGHT_GRAY_BORDER,
            height=game_setting.num_rows * (FIELD_WIDTH + LINE_BETWEEN_FIELDS) + FULL_HEIGHT_TOP_FRAME + BOT_GRAY_BORDER + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER + BOT_FIELD_BORDER + TOP_GRAY_BORDER + TOP_WHITE_BORDER
        )

        # icon and main field
        self._root = tk.Tk()
        self._root.title("Minesweeper")
        self._root.resizable(False, False)
        # tk.Canvas(self._root, bg=COLOR_LIGHT_GRAY, width=self._size.width-MULTIPLIER, height=self._size.height-MULTIPLIER).pack()  # todo rand abschneiden?
        tk.Canvas(self._root, bg=COLOR_LIGHT_GRAY, width=self._size.width, height=self._size.height).pack()
        self._root.wm_iconbitmap(bitmap=utils.resource_path("ui\\icon.ico"))
        self._root._size = self._size

        # images
        self._counter_images = counter.CounterImages()
        self._smiley_images = smiley.SmileyImages()
        self._field_images = field.FieldImages()
        self._panel_images = panel.PanelImages()

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
        self._upper_frame._width = game_setting.num_cols * (FIELD_WIDTH + LINE_BETWEEN_FIELDS) + LEFT_FIELD_BORDER + RIGHT_FIELD_BORDER
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
        self._flag_counter = counter.FlagCounter(flag_counter_frame, self.setting.bombs, self._counter_images)
        self._flag_counter.init()

        # timer counter area
        timer_counter_frame = tk.Frame(self._upper_frame)
        timer_counter_frame.place(x=self._upper_frame._width - COUNTER_WIDTH*3 - SPACER_RIGHT_COUNTER - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=COUNTER_WIDTH * 3, height=COUNTER_HEIGHT)
        top_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER*2 - COUNTER_WIDTH*3 - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=COUNTER_WIDTH*3 + BORDER_AROUND_COUNTER, height=BORDER_AROUND_COUNTER)
        left_border = tk.Label(self._upper_frame, bg=COLOR_TOP_BORDER_COUNTER).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER*2 - COUNTER_WIDTH*3 - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=BORDER_AROUND_COUNTER, height=COUNTER_HEIGHT+BORDER_AROUND_COUNTER)
        right_border = tk.Label(self._upper_frame, bg=COLOR_BOT_BORDER_COUNTER).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=BORDER_AROUND_COUNTER, height=COUNTER_HEIGHT + BORDER_AROUND_COUNTER)
        bottom_border = tk.Label(self._upper_frame, bg=COLOR_BOT_BORDER_COUNTER).place(x=self._upper_frame._width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER - COUNTER_WIDTH*3 - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER + COUNTER_HEIGHT, width=COUNTER_WIDTH*3 + BORDER_AROUND_COUNTER, height=BORDER_AROUND_COUNTER)
        self._timer_counter = counter.TimeCounter(timer_counter_frame, 0, self._counter_images)
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
        self._field_frame._width = game_setting.num_cols * (FIELD_WIDTH + LINE_BETWEEN_FIELDS)
        self._field_frame._height = game_setting.num_rows * (FIELD_WIDTH + LINE_BETWEEN_FIELDS)
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
        self._give_out_bombs()
        self._update_all_fields()

        self._root.mainloop()

    def create_fields(self, ):
        """
        initially create fields and panels and place them on the gamefield
        :return:
        :rtype:
        """
        # create fields
        for col in range(self.setting.num_cols):
            col_fields = []
            for row in range(self.setting.num_rows):
                elem = field.Field(self._field_frame, Position(col, row), self._field_images)
                elem.place()
                elem.add_panel(self._panel_images)
                elem.panel._place()
                col_fields.append(elem)
            self._fields.append(col_fields)

        # todo play with idletasks as one way to improve compute time and generating gamefield to begin with
        # tk.update_idletasks()
        # tk.update()
        # # https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop

    def new_game(self):
        """
        start new game
        :return:
        :rtype:
        """

        # self._timer_counter.start_timer()   # todo

        self._reset_all_fields()
        self._give_out_bombs()
        self._update_all_fields(recalc=True)

    def _give_out_bombs(self):
        """
        randomly select positions for bombs
        :return: None
        :rtype: None
        """
        av_pos = []
        for x in range(self.setting.num_rows):
            for y in range(self.setting.num_cols):
                av_pos.append(Position(x, y))

        bombs = random.sample(av_pos, self.setting.bombs)
        for pos in bombs:
            self._fields[pos.x][pos.y].has_bomb = True

    def _update_all_fields(self, recalc=False):
        """
        updates images on all fields, can also calculate num bombs nearby for all fields
        :return: None
        :rtype: None
        """
        t = time.time()
        if recalc:
            for x in range(self.setting.num_cols):
                for y in range(self.setting.num_rows):
                    import utils

                    sub_field = []
                    if x > 0:
                        sub_field.extend(self._fields[x-1][max(y-1, 0):min(y+2, self.setting.num_rows)])
                    sub_field.extend(self._fields[x][max(y-1, 0):min(y+2, self.setting.num_rows)])
                    if x < self.setting.num_cols-1:
                        sub_field.extend(self._fields[x+1][max(y-1, 0):min(y+2, self.setting.num_rows)])

                    self._fields[x][y].bombs_near = [elem.has_bomb for elem in sub_field].count(True)
                    self._fields[x][y].update_img()
            utils.LOG.debug("This took {}s".format(time.time() - t))

        else:  # no recalc
            for row in self._fields:
                for elem in row:
                    elem.update_img()

    def _reset_all_fields(self):
        """
        resets all fields for a new game with already built gui elements
        :return: None
        :rtype: None
        """
        for row in self._fields:
            for elem in row:
                elem.reset()
