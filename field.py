import tkinter as tk

from classes import Position, Size
import utils
from constants import *


class BackPanelImages(object):

    Empty = None
    Bomb = None
    BombCleared = None
    BombExploded = None
    Cnt_1 = None
    Cnt_2 = None
    Cnt_3 = None
    Cnt_4 = None
    Cnt_5 = None
    Cnt_6 = None
    Cnt_7 = None
    Cnt_8 = None

    def __init__(self):

        self.Empty = utils.get_img("ui\\fields\\empty.png")
        self.Bomb = utils.get_img("ui\\fields\\bomb.png")
        self.BombCleared = utils.get_img("ui\\fields\\bomb_cleared.png")
        self.BombExploded = utils.get_img("ui\\fields\\bomb_exploded.png")
        self.Cnt_1 = utils.get_img("ui\\fields\\1.png")
        self.Cnt_2 = utils.get_img("ui\\fields\\2.png")
        self.Cnt_3 = utils.get_img("ui\\fields\\3.png")
        self.Cnt_4 = utils.get_img("ui\\fields\\4.png")
        self.Cnt_5 = utils.get_img("ui\\fields\\5.png")
        self.Cnt_6 = utils.get_img("ui\\fields\\6.png")
        self.Cnt_7 = utils.get_img("ui\\fields\\7.png")
        self.Cnt_8 = utils.get_img("ui\\fields\\8.png")


class FrontPanelImages(object):

    Panel_img = None
    Flag_img = None

    def __init__(self):

        self.Panel_img = utils.get_img("ui\\fields\\panel.png")
        self.Flag_img = utils.get_img("ui\\fields\\flag.png")


class PanelBC:

    def __init__(self, frame, size, pos, images):
        """
        constructor for panel class
        :param frame: ui frame to place widget in
        :type frame: tk.Frame
        :param size: Size of widget
        :type size: Size:
        :param pos: widget position in gamefield
        :type pos: Position
        :param images: all possible label images
        :type images: FrontPanelImages or BackPanelImages
        """
        self._frame = frame
        self._images = images
        self.size = size
        self.pos = pos

        self._lbl = tk.Label(self._frame)
        self._lbl.image = None

    def place(self):
        """
        abstract method which must be redefined
        :return: None
        :rtype: None
        """
        raise NotImplementedError("Place method not implemented by subclass!")

    def un_place(self):
        """
        abstract method which must be redefined
        :return: None
        :rtype: None
        """
        self._lbl.place_forget()

    def _set_img(self, img):
        """
        helper function to set image to field and save as field variable
        :param img: new image to set
        :type img: tk.PhotoImage
        :return: None
        :rtype: None
        """
        if self._lbl.image != img:
            self._lbl.image = img
            self._lbl.configure(image=self._lbl.image)

    def reset(self):
        """
        abstract method for resetting panel to standard values
        :return: None
        :rtype: None
        """
        raise NotImplementedError("Reset method not implemented by subclass!")


class Front(PanelBC):
    
    def __init__(self, frame, size, pos, images, cb_left_click, cb_right_click):
        """
        Back Panel with flags on it, can be revealed to show back panels
        :param frame: ui frame to place widget in
        :type frame: tk.Frame
        :param size: Size of widget
        :type size: Size:
        :param pos: widget position in game field
        :type pos: Position
        :param images: all possible label images
        :type images: FrontPanelImages
        :param cb_left_click: callback of field class for left click on panel
        :type cb_left_click:
        :param cb_right_click: callback of field class for right click on panel
        :type cb_right_click:
        """
        super(Front, self).__init__(frame, size, pos, images)

        self.has_flag = False
        self.is_revealed = False

        # bound commands
        self._lbl.bind("<Button-1>", lambda event: cb_left_click())
        self._lbl.bind("<Button-2>", lambda event: cb_right_click())
        self._lbl.bind("<Button-3>", lambda event: cb_right_click())

        # todo use this for calling smiley reaction
        # self._lbl.bind("<Button-3>", self.cmd_right_click())
        # self._lbl.bind("<Button-3>", self.cmd_right_click())
        # self._lbl.bind("<Button-3>", self.cmd_right_click())
        # <Button>, <ButtonPress>, or <ButtonRelease>

    def place(self):
        """
        initialize and place panel button
        :return:
        :rtype:
        """
        # if self.is_revealed:
        self.is_revealed = False
        self._lbl.place(x=0 + self.pos.x * FRONT_PANEL_WIDTH, y=0 + self.pos.y * FRONT_PANEL_HEIGHT, width=FRONT_PANEL_WIDTH, height=FRONT_PANEL_HEIGHT)
        if self._lbl.image is None:
            self._set_img(self._images.Panel_img)

    def un_place(self):
        """
        reveal panel
        :return: None
        :rtype: None
        """
        # if not self.is_revealed:
        self.is_revealed = True
        self._lbl.place_forget()

    # @property
    # def revealed(self):
    #     """
    #     property getter of _revealed, returns revealed state
    #     :return: is revealed or not
    #     :rtype: bool
    #     """
    #     return self._is_revealed
    #
    # @revealed.setter
    # def revealed(self, state):
    #     """
    #     property setter for _revealed
    #     :param state: panel is revealed or not
    #     :type state: bool
    #     :return: None
    #     :rtype: None
    #     """
    #     if state and not self._is_revealed:
    #         self.un_place()
    #     elif not state and self._is_revealed:
    #         self.place()

    def set_flag(self):
        """
        sets flag to panel
        :return: None
        :rtype: None
        """
        self.has_flag = True
        self._set_img(self._images.Flag_img)

    def del_flag(self):
        """
        deletes flag from panel
        :return: None
        :rtype: None
        """
        self.has_flag = False
        self._set_img(self._images.Panel_img)

    def reset(self):
        """
        resets back panel to original
        :return: None
        :rtype: None
        """
        self.del_flag()
        self.place()


class Back(PanelBC):

    def __init__(self, frame, size, pos, images):
        """
        Back Panel with numbers and bombs on it
        :param frame: ui frame to place widget in
        :type frame: tk.Frame
        :param size: Size of widget
        :type size: Size:param images:
        :param pos: widget position in gamefield
        :type pos: Position
        :param images: all possible label images
        :type images: BackPanelImages
        """
        super(Back, self).__init__(frame, size, pos, images)
        self._rep_images = {
            None: self._images.Empty,
            0: self._images.Empty,
            1: self._images.Cnt_1,
            2: self._images.Cnt_2,
            3: self._images.Cnt_3,
            4: self._images.Cnt_4,
            5: self._images.Cnt_5,
            6: self._images.Cnt_6,
            7: self._images.Cnt_7,
            8: self._images.Cnt_8
            # 'Bomb': self._images.Bomb,
            # 'Bomb_Cleared': self._images.BombCleared,
            # 'Bomb_Exploded': self._images.BombExploded
        }

        self.has_bomb = False
        self.bombs_near = None

    def place(self):
        """
        initialize labels and place them
        :return: None
        :rtype: None
        """
        self._lbl.place(x=LINE_BETWEEN_FIELDS + self.pos.x * (BACK_PANEL_WIDTH + LINE_BETWEEN_FIELDS), y=LINE_BETWEEN_FIELDS + self.pos.y * (BACK_PANEL_HEIGHT + LINE_BETWEEN_FIELDS), width=BACK_PANEL_WIDTH, height=BACK_PANEL_HEIGHT)

    def update_img(self):
        """
        updates image based on settings
        :return: None
        :rtype: None
        """
        if self.has_bomb:
            self._set_img(self._images.Bomb)
        else:
            self._set_img(self._rep_images[self.bombs_near])

    def set_bomb(self):
        """
        sets new bomb to back field
        :return: None
        :rtype: None
        """
        self.has_bomb = True
        self._set_img(self._images.Bomb)

    def set_exploded_bomb(self):
        """
        sets exploded bomb to back field
        :return: None
        :rtype: None
        """
        self._set_img(self._images.BombExploded)

    def set_disarmed_bomb(self):
        """
        sets disarmed bomb to back field
        :return: None
        :rtype: None
        """
        self._set_img(self._images.BombCleared)

    def reset(self):
        """
        resets back panel to original
        :return: None
        :rtype: None
        """
        self.has_bomb = False
        self.bombs_near = None


class Field(object):
    """
    represents one field in the game field
    """

    def __init__(self, pos, game_status, cb_flag_up, cb_flag_down, cb_start_timer, cb_reveal_empty_fields, cb_game_won, cb_game_lost):
        """
        :param pos: Position of field inside game field
        :type pos: Position
        :param game_status: game status with global flags
        :type game_status: GameStatus
        :param cb_flag_down: callback to count counter for flag counter up
        :type cb_flag_down:
        :param cb_flag_up: callback to count counter for flag counter down
        :type cb_flag_up:
        :param cb_start_timer: callback for stopping game time counter
        :type cb_start_timer:
        :param cb_reveal_empty_fields: callback for revealing non numbered fields
        :type cb_reveal_empty_fields:
        :param cb_game_lost: callback when hitting an uncovered bomb, ends game
        :type cb_game_lost:
        :param cb_game_won: callback when revealing the last numbered or empty field, game is won
        :type cb_game_won:
        """
        self.logger = utils.get_logger(self.__class__.__name__)  # todo raus?  oder überall rein

        self.pos = pos
        self.game_status = game_status
        self.front: Front = None
        self.back: Back = None

        # callbacks from gui class
        self._cb_flag_cnt_up = cb_flag_up
        self._cb_flag_cnt_down = cb_flag_down
        self._cb_start_timer = cb_start_timer
        self._cb_reveal_empty_fields = cb_reveal_empty_fields
        self._cb_game_won = cb_game_won
        self._cb_game_lost = cb_game_lost

    def add_front(self, frame, pos, images):
        """
        Adds front panel to field with label showing flags and holding callbacks
        :param frame: ui frame to place widget in
        :type frame: tk.Frame
        :param pos: position of front panel inside game field
        :type pos: Position
        :param images: all possible images for front panel
        :type images: FrontPanelImages
        :return: None
        :rtype: None
        """
        self.front = Front(frame, Size(FRONT_PANEL_HEIGHT, FRONT_PANEL_WIDTH), pos, images, self.cmd_left_click, self.cmd_right_click)

    def add_back(self, frame, pos, images):
        """
        Adds back panel to field with label showing numbers and bombs
        :param frame: ui frame to place widget in
        :type frame: tk.Frame
        :param pos: position of back panel inside game field
        :type pos: Position
        :param images: all possible images for back panel
        :type images: BackPanelImages
        :return: None
        :rtype: None
        """
        self.back = Back(frame, Size(BACK_PANEL_HEIGHT, BACK_PANEL_WIDTH), pos, images)

    def reset(self):
        """
        resets field to standard values
        :return: None
        :rtype: None
        """
        self.back.reset()
        self.front.reset()

    def cmd_right_click(self):
        """
        command for right click on panel, sets or releases flag
        :return: None
        :rtype: None
        """
        if self.game_status.running:
            if self.front.has_flag:
                self.front.del_flag()
                self._cb_flag_cnt_up()
            else:
                self.front.set_flag()
                self._cb_flag_cnt_down()

    def cmd_left_click(self):
        """
        command for left click on panel, reveals the field behind it
        :return: None
        :rtype: None
        """
        if self.game_status.running and not self.front.has_flag:

            self._cb_start_timer()  # starts game time counter if not already running
            self.revealed = True

            # when hitting a bomb game is lost
            if self.back.has_bomb:
                self.back.set_exploded_bomb()
                self._cb_game_lost()

            # when hitting a uncovered field all fields around are exposed
            if self.back.bombs_near == 0:
                self._cb_reveal_empty_fields(self.pos)

    @property
    def revealed(self):
        """
        property getter of _revealed, returns self.is_revealed state
        :return: is revealed or not
        :rtype: bool
        """
        return self.front.is_revealed

    @revealed.setter
    def revealed(self, state):
        """
        property setter for _revealed
        :param state: panel is revealed or not
        :type state: bool
        :return: None
        :rtype: None
        """
        if state and not self.front.is_revealed:
            self.front.un_place()

            # handle counter towards game won
            if not self.back.has_bomb:
                self.game_status.fields_left -= 1
                if self.game_status.fields_left == 0:
                    self._cb_game_won()

        elif not state and self.front.is_revealed:
            self.front.place()

    def __eq__(self, other):
        return self.pos == other.pos

    def __ne__(self, other):
        return self.pos != other.pos
