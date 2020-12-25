
import tkinter as tk

import utils
from constants import PANEL_HEIGHT, PANEL_WIDTH
from classes import Size


class PanelImages(object):

    Panel_img = None
    Flag_img = None

    def __init__(self):

        self.Panel_img = utils.get_img("ui\\fields\\panel.png")
        self.Flag_img = utils.get_img("ui\\fields\\flag.png")


class Panel(object):
    """"
    represents a panel in the field above the field uni
    """

    size = Size(width=PANEL_WIDTH, height=PANEL_HEIGHT)

    def __init__(self, frame, pos, images, cb_flag_up, cb_flag_down, cb_start_timer, cb_stop_timer):
        """
        # todo paramter beschreiben, auch callbacks
        :param frame:
        :type frame: tk.Frame
        :param pos:
        :type pos: Position
        :param images:
        :type images: PanelImages
        """
        self._frame = frame
        self.pos = pos
        self._images = images

        self._cb_flag_cnt_up = cb_flag_up
        self._cb_flag_cnt_down = cb_flag_down
        self._cb_start_timer = cb_start_timer
        self._cb_stop_timer = cb_stop_timer
        self._cb_game_lost = None
        self._cb_explode_bomb = None

        self._lbl = tk.Label(self._frame, bd=0, image=self._images.Panel_img)
        self._lbl.image = self._images.Panel_img
        self._lbl.bind("<Button-1>", lambda event: self.cmd_left_click())
        self._lbl.bind("<Button-2>", lambda event: self.cmd_right_click())
        self._lbl.bind("<Button-3>", lambda event: self.cmd_right_click())

        # todo use this for calling smiley reaction
        # self._lbl.bind("<Button-3>", self.cmd_right_click())
        # self._lbl.bind("<Button-3>", self.cmd_right_click())
        # self._lbl.bind("<Button-3>", self.cmd_right_click())
        # <Button>, <ButtonPress>, or <ButtonRelease>

        self.has_flag = False
        self._revealed = False

    @property
    def reveal(self):
        """
        property getter of _revealed, returns reveald state
        :return: is revealed or not
        :rtype: bool
        """
        return self._revealed

    @reveal.setter
    def reveal(self, state):
        """
        property setter for _revealed
        :param state: panel is revealed or not
        :type state: bool
        :return: None
        :rtype: None
        """
        if state and not self._revealed:
            self.un_place()
        elif not state and self._revealed:
            self.place()

    def cmd_right_click(self):
        """
        command for right click on panel, sets or releases flag
        :return: None
        :rtype: None
        """
        if self.has_flag:
            self._del_flag()
            self._cb_flag_cnt_up()
        else:
            self._set_flag()
            self._cb_flag_cnt_down()

    def cmd_left_click(self):
        """
        command for left click on panel, reveals the field behind it
        :return: None
        :rtype: None
        """
        if not self.has_flag:
            self._cb_start_timer()  # starts game time counter if not already running
            self.reveal = True

            if self._cb_game_lost is not None:  # if callback is not None then there is a bomb
                self._cb_explode_bomb()
                self._cb_game_lost()
                # todo hier noch das feld mit der bombe als exploded markieren




            # todo reveal those next to it as well


    def cmd_on_click(self):
        # todo handle here smiley face on click movement
        pass

    def place(self):
        """
        initialize and place panel button
        :return:
        :rtype:
        """
        self._revealed = False
        self._lbl.place(x=0 + self.pos.x * PANEL_WIDTH, y=0 + self.pos.y * PANEL_HEIGHT, width=PANEL_WIDTH, height=PANEL_HEIGHT)

    def un_place(self):
        """
        reveal panel
        :return: None
        :rtype: None
        """
        self._revealed = True
        self._lbl.place_forget()

    def _set_flag(self):
        """
        sets flag to panel
        :return: None
        :rtype: None
        """
        self.has_flag = True
        self._set_img(self._images.Flag_img)

    def _del_flag(self):
        """
        deletes flag from panel
        :return: None
        :rtype: None
        """
        self.has_flag = False
        self._set_img(self._images.Panel_img)

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
