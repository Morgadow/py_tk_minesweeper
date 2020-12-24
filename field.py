import tkinter as tk

from classes import Position, Size
import utils
import panel
from constants import *


class FieldImages(object):

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


class Field(object):
    """
    represents one field in the game field
    """

    size = Size(width=FIELD_WIDTH, height=FIELD_HEIGHT)

    def __init__(self, frame, pos, images):
        """

        :param frame:
        :type frame: tk.Frame
        :param pos:
        :type pos: Position
        :param images:
        :type images: FieldImages
        """
        self._frame = frame
        self.pos = pos
        self._images = images
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

        self._lbl = tk.Label(self._frame, text=str(self.pos))
        self._lbl.image = None
        self.has_bomb = False
        self.bombs_near = None
        self.panel = None

    def place(self):
        """
        initialize labels and place them
        :return: None
        :rtype: None
        """
        self._lbl.place(x=LINE_BETWEEN_FIELDS + self.pos.x * (FIELD_WIDTH + LINE_BETWEEN_FIELDS), y=LINE_BETWEEN_FIELDS + self.pos.y * (FIELD_HEIGHT + LINE_BETWEEN_FIELDS), width=FIELD_WIDTH, height=FIELD_HEIGHT)

    def add_panel(self, images):
        """
        Add overlying panel to the field
        :param images:
        :type images: panel.PanelImages
        :return: None
        :rtype: None
        """
        self.panel = panel.Panel(self._frame, self.pos, images)

    def update_img(self):
        """
        updates image based on settings
        :return: None
        :rtype: None
        """
        # todo add bomb cleared after game ends
        if self.has_bomb:
            self._set_img(self._images.Bomb)
        else:
            self._set_img(self._rep_images[self.bombs_near])

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

    def explode_bomb(self):
        """
        set image to bomb exploded
        :return: None
        :rtype: None
        """
        self._set_img(self._images.Bomb)

    def reset(self):
        """
        resets field and panel above
        :return: None
        :rtype: None
        """
        self.has_bomb = False
        self.bombs_near = None
        self.panel.reveal = False

