
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

    def __init__(self, frame, pos, images):
        """

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

        self._btn = tk.Button(self._frame, bd=0, image=self._images.Panel_img, command=lambda: 'todo')
        self._btn.image = self._images.Panel_img
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
            self._un_place()
            return

        if not state and self._revealed:
            self._place()

    def _place(self):
        """
        initialize and place panel button
        :return:
        :rtype:
        """
        self._btn.place(x=0 + self.pos.x*PANEL_WIDTH, y=0 + self.pos.y*PANEL_HEIGHT, width=PANEL_WIDTH, height=PANEL_HEIGHT)

    def _un_place(self):
        """
        reveal panel
        :return: None
        :rtype: None
        """
        self._btn.place_forget()

    def set_flag(self):
        """
        sets flag to panel
        :return: None
        :rtype: None
        """
        self._set_img(self._images.Flag_img)

    def del_flag(self):
        """
        deletes flag from panel
        :return: None
        :rtype: None
        """
        self._set_img(self._images.Panel_img)

    def _set_img(self, img):
        """
        helper function to set image to field and save as field variable
        :param img: new image to set
        :type img: tk.PhotoImage
        :return: None
        :rtype: None
        """
        if self._btn._image != img:
            self._btn._image = img
            self._btn.configure(image=self._btn._image)
