#!/usr/bin/python3.7
# -*- coding: utf-8 -*-


import sys
import random
import tkinter as tk
import time

import utils
import field
import smiley
import counter
from classes import Size, Position, Game


"""
Main GUI for Minesweeper game
Game mechanics are implemented here and given to other objects as callbacks

DEBUG Mode possible for developing, called by keyword [--debug] as sys argument
"""


# debug mode evaluation, enabling some more printouts, enabling console
DEBUG = (True if '--debug' in sys.argv else False)


# constants of gui sizes
HEIGHT_MENU_BAR = 20

# outer borders of complete field
TOP_WHITE_BORDER = 3  # color: #ffffff
TOP_GRAY_BORDER = 6  # color: #c0c0c0
LEFT_WHITE_BORDER = 3  # color: #c0c0c0
LEFT_GRAY_BORDER = 6  # color: #c0c0c0
RIGHT_GRAY_BORDER = 5  # color: #c0c0c0
BOTTOM_GRAY_BORDER = 5  # color: #c0c0c0
BORDER_TOP_FIELD_BORDER = 6  # color: #c0c0c0

# top frame
OUTER_BORDER_TOP_FRAME = 1
INNER_BORDER_TOP_FRAME = 1
SPACER_ABOVE_COUNTER = 4
SPACER_LEFT_COUNTER = 5
SPACER_RIGHT_COUNTER = 7
SPACER_BELOW_COUNTER = 4
BORDER_AROUND_COUNTER = 1
FULL_HEIGHT_TOP_FRAME = OUTER_BORDER_TOP_FRAME*2 + INNER_BORDER_TOP_FRAME*2 + SPACER_ABOVE_COUNTER + SPACER_BELOW_COUNTER + counter.COUNTER_HEIGHT + BORDER_AROUND_COUNTER*2

# borders around game field
TOP_FIELD_BORDER_1, TOP_FIELD_BORDER_2, TOP_FIELD_BORDER_3 = 1, 1, 1
TOP_FIELD_BORDER = TOP_FIELD_BORDER_1 + TOP_FIELD_BORDER_2 + TOP_FIELD_BORDER_3
LEFT_FIELD_BORDER_1, LEFT_FIELD_BORDER_2, LEFT_FIELD_BORDER_3 = 1, 1, 1
LEFT_FIELD_BORDER = LEFT_FIELD_BORDER_1 + LEFT_FIELD_BORDER_2 + LEFT_FIELD_BORDER_3
RIGHT_FIELD_BORDER_1, RIGHT_FIELD_BORDER_2, RIGHT_FIELD_BORDER_3 = 1, 1, 1
RIGHT_FIELD_BORDER = RIGHT_FIELD_BORDER_1 + RIGHT_FIELD_BORDER_2 + RIGHT_FIELD_BORDER_3
BOT_FIELD_BORDER_1, BOT_FIELD_BORDER_2, BOT_FIELD_BORDER_3 = 1, 1, 1
BOT_FIELD_BORDER = BOT_FIELD_BORDER_1 + BOT_FIELD_BORDER_2 + BOT_FIELD_BORDER_3


# colors (retrieved by screenshotting and color matching done in MSPaint)
COLOR_WHITE = '#FFFFFF'
COLOR_LIGHT_GRAY = '#c0c0c0'
COLOR_DARK_GRAY = '#808080'


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


class MinesweeperGUI:
    """
    Main Minesweeper game GUI building all objects and elements needed for game, all game mechanics are implemented here
    """

    # noinspection PyTypeChecker
    def __init__(self, game, cb_change_field):

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
        self._cb_change_field = cb_change_field

        # images for game elements
        self._counter_images: counter.CounterImages = None
        self._smiley_images: smiley.SmileyImages = None
        self._field_front_images: field.FrontPanelImages = None
        self._field_back_images: field.BackPanelImages = None

        # debug handling
        if DEBUG:
            self._debug_reveal = False
            self._debug_revealed_fields = []

    def build_gui(self):
        """
        main function to build main gui
        :return: None
        :rtype: None
        """
        # basic settings
        self._size = Size(
            width=self.game.curr_setting.num_cols * (field.BACK_PANEL_WIDTH + field.LINE_BETWEEN_FIELDS) + RIGHT_FIELD_BORDER + LEFT_FIELD_BORDER + LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + RIGHT_GRAY_BORDER,
            height=self.game.curr_setting.num_rows * (field.BACK_PANEL_WIDTH + field.LINE_BETWEEN_FIELDS) + TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + BOTTOM_GRAY_BORDER + TOP_FIELD_BORDER + BOT_FIELD_BORDER
        )

        # icon and main field
        self._root = tk.Tk()
        self._root.geometry("{}x{}".format(self._size.width, self._size.height + HEIGHT_MENU_BAR))
        self._root.title("Minesweeper")
        self._root.resizable(False, False)
        tk.Canvas(self._root, bg=COLOR_LIGHT_GRAY, width=self._size.width, height=self._size.height).pack()
        self._root.wm_iconbitmap(bitmap=utils.resource_path("ui\\icon.ico"))
        self._root.size = self._size
        self._root.bind("<F2>", lambda event: self.new_game())

        # debug binds
        if DEBUG:
            self._root.bind("<F3>", lambda event: self._debug_print_sizes())
            self._root.bind("<F4>", lambda event: self._debug_reveal_field())

        # menu bar
        menu = tk.Menu(self._root, tearoff=0)
        self._root.config(menu=menu)

        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Game', menu=game_menu)
        game_menu.add_command(label='New                        F2', command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label='Beginner', command=lambda: self._cb_change_field(self.game.possible_settings['Beginner']))
        game_menu.add_command(label='Intermediate', command=lambda: self._cb_change_field(self.game.possible_settings['Intermediate']))
        game_menu.add_command(label='Expert', command=lambda: self._cb_change_field(self.game.possible_settings['Expert']))
        game_menu.add_command(label='Custom')  # todo
        game_menu.add_separator()
        game_menu.add_command(label='Marks (?)')
        game_menu.add_command(label='Colour')
        game_menu.add_command(label='Sound')
        game_menu.add_separator()
        game_menu.add_command(label='Best Times')
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self._root.quit)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Contents                        F1')
        help_menu.add_command(label='Search for Help on...')
        help_menu.add_command(label='Using Help')
        help_menu.add_separator()
        help_menu.add_command(label='About Minesweeper')

        # images
        self._counter_images = counter.CounterImages()
        self._smiley_images = smiley.SmileyImages()
        self._field_front_images = field.FrontPanelImages()
        self._field_back_images = field.BackPanelImages()

        # main borders, white and gray
        tk.Label(self._root, bg=COLOR_WHITE).place(x=0, y=0, height=TOP_WHITE_BORDER, width=self._size.width)
        tk.Label(self._root, bg=COLOR_WHITE).place(x=0, y=0, height=self._size.height, width=LEFT_WHITE_BORDER)
        tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=LEFT_WHITE_BORDER, y=TOP_WHITE_BORDER, width=self._size.width - LEFT_WHITE_BORDER, height=TOP_GRAY_BORDER)
        tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=LEFT_WHITE_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER, width=LEFT_GRAY_BORDER, height=self._size.height - TOP_WHITE_BORDER - TOP_GRAY_BORDER)
        tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME, width=self._size.width - LEFT_GRAY_BORDER - LEFT_WHITE_BORDER - RIGHT_GRAY_BORDER, height=BORDER_TOP_FIELD_BORDER)
        tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=self._size.width - RIGHT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER, width=RIGHT_GRAY_BORDER, height=self._size.height - TOP_GRAY_BORDER - TOP_WHITE_BORDER)
        tk.Label(self._root, bg=COLOR_LIGHT_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=self._size.height - BOTTOM_GRAY_BORDER, width=self._size.width - LEFT_GRAY_BORDER - LEFT_WHITE_BORDER - RIGHT_GRAY_BORDER, height=BOTTOM_GRAY_BORDER)

        # upper area
        self._upper_frame = tk.Frame(self._root, bg=COLOR_LIGHT_GRAY)
        self._upper_frame.width = self.game.curr_setting.num_cols * (field.BACK_PANEL_WIDTH + field.LINE_BETWEEN_FIELDS) + LEFT_FIELD_BORDER + RIGHT_FIELD_BORDER
        self._upper_frame.height = FULL_HEIGHT_TOP_FRAME
        self._upper_frame.place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER, width=self._upper_frame.width, height=self._upper_frame.height)

        # outer borders around upper area
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=0, y=0, width=self._upper_frame.width - OUTER_BORDER_TOP_FRAME, height=OUTER_BORDER_TOP_FRAME)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=0, y=OUTER_BORDER_TOP_FRAME*2, width=OUTER_BORDER_TOP_FRAME, height=self._upper_frame.height - OUTER_BORDER_TOP_FRAME * 3)
        tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=self._upper_frame.width - OUTER_BORDER_TOP_FRAME, y=OUTER_BORDER_TOP_FRAME, width=OUTER_BORDER_TOP_FRAME, height=self._upper_frame.height - OUTER_BORDER_TOP_FRAME)
        tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=OUTER_BORDER_TOP_FRAME, y=self._upper_frame.height - OUTER_BORDER_TOP_FRAME, width=self._upper_frame.width - OUTER_BORDER_TOP_FRAME * 3, height=OUTER_BORDER_TOP_FRAME)

        # inner borders around upper area
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=0, y=OUTER_BORDER_TOP_FRAME, width=self._upper_frame.width - OUTER_BORDER_TOP_FRAME * 2, height=OUTER_BORDER_TOP_FRAME)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=OUTER_BORDER_TOP_FRAME, y=OUTER_BORDER_TOP_FRAME*2, width=OUTER_BORDER_TOP_FRAME, height=self._upper_frame.height - OUTER_BORDER_TOP_FRAME * 4)
        tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=self._upper_frame.width - OUTER_BORDER_TOP_FRAME * 2, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME, width=OUTER_BORDER_TOP_FRAME, height=self._upper_frame.height - OUTER_BORDER_TOP_FRAME * 2)
        tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=OUTER_BORDER_TOP_FRAME*2, y=self._upper_frame.height - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME, width=self._upper_frame.width - OUTER_BORDER_TOP_FRAME * 4, height=OUTER_BORDER_TOP_FRAME)

        # flag counter area
        flag_counter_frame = tk.Frame(self._upper_frame)
        flag_counter_frame.place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER + BORDER_AROUND_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=counter.COUNTER_WIDTH * 3, height=counter.COUNTER_HEIGHT)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=counter.COUNTER_WIDTH*3, height=BORDER_AROUND_COUNTER)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=BORDER_AROUND_COUNTER, height=counter.COUNTER_HEIGHT+BORDER_AROUND_COUNTER)
        tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER + counter.COUNTER_WIDTH*3, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=BORDER_AROUND_COUNTER, height=counter.COUNTER_HEIGHT + BORDER_AROUND_COUNTER)
        tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_LEFT_COUNTER + BORDER_AROUND_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER + counter.COUNTER_HEIGHT, width=counter.COUNTER_WIDTH*3, height=BORDER_AROUND_COUNTER)
        self._flag_counter = counter.FlagCounter(flag_counter_frame, self.game.curr_setting.bombs, self._counter_images, self.game)
        self._flag_counter.init()

        # timer counter area
        timer_counter_frame = tk.Frame(self._upper_frame)
        timer_counter_frame.place(x=self._upper_frame.width - counter.COUNTER_WIDTH * 3 - SPACER_RIGHT_COUNTER - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=counter.COUNTER_WIDTH * 3, height=counter.COUNTER_HEIGHT)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=self._upper_frame.width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER * 2 - counter.COUNTER_WIDTH * 3 - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=counter.COUNTER_WIDTH * 3 + BORDER_AROUND_COUNTER, height=BORDER_AROUND_COUNTER)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=self._upper_frame.width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER * 2 - counter.COUNTER_WIDTH * 3 - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER, width=BORDER_AROUND_COUNTER, height=counter.COUNTER_HEIGHT + BORDER_AROUND_COUNTER)
        tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=self._upper_frame.width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER, width=BORDER_AROUND_COUNTER, height=counter.COUNTER_HEIGHT + BORDER_AROUND_COUNTER)
        tk.Label(self._upper_frame, bg=COLOR_WHITE).place(x=self._upper_frame.width - OUTER_BORDER_TOP_FRAME - INNER_BORDER_TOP_FRAME - BORDER_AROUND_COUNTER - counter.COUNTER_WIDTH * 3 - SPACER_RIGHT_COUNTER, y=OUTER_BORDER_TOP_FRAME + INNER_BORDER_TOP_FRAME + SPACER_ABOVE_COUNTER + BORDER_AROUND_COUNTER + counter.COUNTER_HEIGHT, width=counter.COUNTER_WIDTH * 3 + BORDER_AROUND_COUNTER, height=BORDER_AROUND_COUNTER)
        self._timer_counter = counter.TimeCounter(timer_counter_frame, 0, self._counter_images, self.game)
        self._timer_counter.init()

        # smiley
        smiley_frame = tk.Frame(self._upper_frame)
        smiley_frame.place(x=(self._upper_frame.width - smiley.SMILEY_WIDTH) / 2, y=(FULL_HEIGHT_TOP_FRAME - smiley.SMILEY_HEIGHT) / 2, width=smiley.SMILEY_WIDTH, height=smiley.SMILEY_HEIGHT)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=(self._upper_frame.width - smiley.SMILEY_WIDTH) / 2 - smiley.SMILEY_BORDER, y=(FULL_HEIGHT_TOP_FRAME - smiley.SMILEY_HEIGHT) / 2 - smiley.SMILEY_BORDER, width=smiley.SMILEY_WIDTH + smiley.SMILEY_BORDER, height=smiley.SMILEY_BORDER)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=(self._upper_frame.width - smiley.SMILEY_WIDTH) / 2 - smiley.SMILEY_BORDER, y=(FULL_HEIGHT_TOP_FRAME - smiley.SMILEY_HEIGHT) / 2, width=smiley.SMILEY_BORDER, height=smiley.SMILEY_HEIGHT)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=(self._upper_frame.width - smiley.SMILEY_WIDTH) / 2 + smiley.SMILEY_WIDTH, y=(FULL_HEIGHT_TOP_FRAME - smiley.SMILEY_HEIGHT) / 2, width=smiley.SMILEY_BORDER, height=smiley.SMILEY_HEIGHT + smiley.SMILEY_BORDER)
        tk.Label(self._upper_frame, bg=COLOR_DARK_GRAY).place(x=(self._upper_frame.width - smiley.SMILEY_WIDTH) / 2, y=(FULL_HEIGHT_TOP_FRAME - smiley.SMILEY_HEIGHT) / 2 + smiley.SMILEY_HEIGHT, width=smiley.SMILEY_WIDTH + smiley.SMILEY_BORDER, height=smiley.SMILEY_BORDER)
        self._smiley = smiley.Smiley(smiley_frame, self._smiley_images, cb_new_game=self.new_game)
        self._smiley.init()

        # field area
        self._field_frame = tk.Frame(self._root, bg=COLOR_DARK_GRAY)
        self._field_frame.width = self.game.curr_setting.num_cols * (field.BACK_PANEL_WIDTH + field.LINE_BETWEEN_FIELDS)
        self._field_frame.height = self.game.curr_setting.num_rows * (field.BACK_PANEL_WIDTH + field.LINE_BETWEEN_FIELDS)
        self._field_frame.place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=self._field_frame.width, height=self._field_frame.height)

        # top, left, right, bot borders around game field
        tk.Label(self._root, bg=COLOR_DARK_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER, width=self._field_frame.width + LEFT_FIELD_BORDER + RIGHT_FIELD_BORDER_1 + RIGHT_FIELD_BORDER_2, height=TOP_FIELD_BORDER_1)
        tk.Label(self._root, bg=COLOR_DARK_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER_1, width=self._field_frame.width + LEFT_FIELD_BORDER + RIGHT_FIELD_BORDER_1, height=TOP_FIELD_BORDER_2)
        tk.Label(self._root, bg=COLOR_DARK_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER_1 + TOP_FIELD_BORDER_2, width=self._field_frame.width + LEFT_FIELD_BORDER, height=TOP_FIELD_BORDER_3)
        tk.Label(self._root, bg=COLOR_DARK_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=LEFT_FIELD_BORDER_1, height=self._field_frame.height + BOT_FIELD_BORDER_3 + BOT_FIELD_BORDER_2)
        tk.Label(self._root, bg=COLOR_DARK_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER_1, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=LEFT_FIELD_BORDER_2, height=self._field_frame.height + BOT_FIELD_BORDER_3)
        tk.Label(self._root, bg=COLOR_DARK_GRAY).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER_1 + LEFT_FIELD_BORDER_2, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=LEFT_FIELD_BORDER_3, height=self._field_frame.height)
        tk.Label(self._root, bg=COLOR_WHITE).place(x=self._root.size.width - RIGHT_GRAY_BORDER - RIGHT_FIELD_BORDER, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER, width=RIGHT_FIELD_BORDER_1, height=self._field_frame.height)
        tk.Label(self._root, bg=COLOR_WHITE).place(x=self._root.size.width - RIGHT_GRAY_BORDER - RIGHT_FIELD_BORDER_3 - RIGHT_FIELD_BORDER_2, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER_1 + TOP_FIELD_BORDER_2, width=RIGHT_FIELD_BORDER_2, height=self._field_frame.height + TOP_FIELD_BORDER_1)
        tk.Label(self._root, bg=COLOR_WHITE).place(x=self._root.size.width - RIGHT_GRAY_BORDER - RIGHT_FIELD_BORDER_3, y=TOP_WHITE_BORDER + TOP_GRAY_BORDER + FULL_HEIGHT_TOP_FRAME + BORDER_TOP_FIELD_BORDER + TOP_FIELD_BORDER_1, width=RIGHT_FIELD_BORDER_3, height=self._field_frame.height + TOP_FIELD_BORDER_1 + TOP_FIELD_BORDER_2)
        tk.Label(self._root, bg=COLOR_WHITE).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER, y=self._root.size.height - BOTTOM_GRAY_BORDER - BOT_FIELD_BORDER, width=self._field_frame.width + RIGHT_FIELD_BORDER, height=BOT_FIELD_BORDER_1)
        tk.Label(self._root, bg=COLOR_WHITE).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER_1 + LEFT_FIELD_BORDER_2, y=self._root.size.height - BOTTOM_GRAY_BORDER - BOT_FIELD_BORDER_3 - BOT_FIELD_BORDER_2, width=self._field_frame.width + RIGHT_FIELD_BORDER + LEFT_FIELD_BORDER_3, height=BOT_FIELD_BORDER_2)
        tk.Label(self._root, bg=COLOR_WHITE).place(x=LEFT_WHITE_BORDER + LEFT_GRAY_BORDER + LEFT_FIELD_BORDER_1, y=self._root.size.height - BOTTOM_GRAY_BORDER - BOT_FIELD_BORDER_3, width=self._field_frame.width + RIGHT_FIELD_BORDER + LEFT_FIELD_BORDER_3 + LEFT_FIELD_BORDER_2, height=BOT_FIELD_BORDER_3)

        # create fields and panels and prepare everything
        self._create_fields()
        self.new_game()

        self._root.mainloop()

    def _debug_print_sizes(self):
        """
        Debug: prints sizes for geometry and window
        :return: None
        :rtype: None
        """
        print("\nCurrent Sizes:")
        print("Total Width without Menu bar: ", self._root.winfo_width())
        print("Total Height without Menu bar: ", self._root.winfo_height())
        print("Total Width with additional border (???): ", self._root.winfo_reqwidth())
        print("Total Height with Menu bar: ", self._root.winfo_reqheight())
        print("Calculated width: ", self._size.width)
        print("Calculated height: ", self._size.height)

    def _debug_reveal_field(self):
        """
        reveals all bombs until bind pressed again to unrevealed elements, does not effect game status
        :return: None
        :rtype: None
        """
        if self._debug_reveal:
            while len(self._debug_revealed_fields):
                elem = self._debug_revealed_fields.pop()
                self._fields[elem.x][elem.y].front.place()
            self._debug_reveal = False
        else:
            self._debug_reveal = True
            for x in range(self.game.curr_setting.num_cols):
                for y in range(self.game.curr_setting.num_rows):
                    if not self._fields[x][y].front.is_revealed:
                        self._fields[x][y].front.un_place()
                        self._debug_revealed_fields.append(self._fields[x][y].pos)

    def _create_fields(self, ):
        """
        initially create fields and panels and place them on the game field
        :return:
        :rtype:
        """
        t = time.time()
        # create fields
        for col in range(self.game.curr_setting.num_cols):
            col_fields = []
            for row in range(self.game.curr_setting.num_rows):

                elem = field.Field(Position(col, row), self.game, self._flag_counter.count_up, self._flag_counter.count_down, self._timer_counter.start_timer, self.reveal_emtpy_panels, self.game_won, self.game_lost)
                elem.add_back(self._field_frame, elem.pos, self._field_back_images)
                elem.add_front(self._field_frame, elem.pos, self._field_front_images)
                elem.back.place()
                elem.front.place()

                col_fields.append(elem)
            self._fields.append(col_fields)

        utils.LOG.debug("Creating all fields took: {}s".format(time.time() - t))
        # todo play with idletasks as one way to improve compute time and generating game field to begin with
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
        self._update_all_fields(eval_nums=True)
        self._timer_counter.reset()
        self._flag_counter.reset(start=self.game.curr_setting.bombs)
        self.game.running = True
        self.game.fields_left = self.game.curr_setting.num_rows * self.game.curr_setting.num_rows - self.game.curr_setting.bombs

    def _give_out_bombs(self):
        """
        randomly select positions for bombs out of all possible positions
        :return: None
        :rtype: None
        """
        av_pos = []
        for x in range(self.game.curr_setting.num_cols):
            for y in range(self.game.curr_setting.num_rows):
                av_pos.append(Position(x, y))

        bombs = random.sample(av_pos, self.game.curr_setting.bombs)
        for pos in bombs:
            self._fields[pos.x][pos.y].back.set_bomb()

    def _update_all_fields(self, eval_nums=False):
        """
        updates images on all back fields, can also calculate num bombs nearby for all fields
        :param eval_nums: if set all back field numbers are recalculated
        :type eval_nums: bool
        :return: None
        :rtype: None
        """
        t = time.time()
        if eval_nums:
            for x in range(self.game.curr_setting.num_cols):
                for y in range(self.game.curr_setting.num_rows):

                    sub_field = []
                    if x > 0:
                        sub_field.extend(self._fields[x-1][max(y-1, 0):min(y + 2, self.game.curr_setting.num_rows)])
                    sub_field.extend(self._fields[x][max(y-1, 0):min(y + 2, self.game.curr_setting.num_rows)])
                    if x < self.game.curr_setting.num_cols-1:
                        sub_field.extend(self._fields[x+1][max(y-1, 0):min(y + 2, self.game.curr_setting.num_rows)])

                    self._fields[x][y].back.bombs_near = [elem.back.has_bomb for elem in sub_field].count(True)
                    self._fields[x][y].back.update_img()

            utils.LOG.debug("calculating numbers took {}s".format(time.time() - t))

        else:  # no calculation of bombs nearby
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

        for x in range(self.game.curr_setting.num_cols):  # every unflagged bomb gets a flag
            for y in range(self.game.curr_setting.num_rows):
                if self._fields[x][y].back.has_bomb and not self._fields[x][y].front.has_flag:
                    self._fields[x][y].front.set_flag()

        # todo handle highscore

    def reveal_bombs(self):
        """
        removes front panels and reveals bombs behind, used at game lost showing remaining and cleared bombs
        :return: None
        :rtype: None
        """
        for x in range(self.game.curr_setting.num_cols):
            for y in range(self.game.curr_setting.num_rows):
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
            sub_field.extend(self._fields[pos.x-1][max(pos.y-1, 0):min(pos.y + 2, self.game.curr_setting.num_rows)])
        if pos.x < self.game.curr_setting.num_cols-1:
            sub_field.extend(self._fields[pos.x+1][max(pos.y-1, 0):min(pos.y + 2, self.game.curr_setting.num_rows)])
        if pos.y > 0:
            sub_field.append(self._fields[pos.x][pos.y-1])
        if pos.y < self.game.curr_setting.num_rows-1:
            sub_field.append(self._fields[pos.x][pos.y+1])

        return sub_field

    def destroy(self):
        """
        destroy complete field and all containing elements for rebuilding purposes
        :return: None
        :rtype: None
        """
        if self._root is not None:
            self._root.destroy()
