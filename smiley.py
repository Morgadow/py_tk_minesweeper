
import threading
import tkinter as tk
import utils
from constants import SMILEY_WIDTH, SMILEY_HEIGHT


class SmileyImages(object):
    """
    all possible images for counter fields for faster image setting
    """
    smiley_start = None
    smiley_lost = None
    smiley_won = None
    smiley_on_click = None

    def __init__(self):

        self.smiley_start = utils.get_img("ui\\smiley\\smiley.png")
        self.smiley_lost = utils.get_img("ui\\smiley\\smiley_lost.png")
        self.smiley_won = utils.get_img("ui\\smiley\\smiley_won.png")
        self.smiley_on_click = utils.get_img("ui\\smiley\\smiley_onclick.png")


class Smiley(object):

    def __init__(self, frame, images, cb):
        """

        :param frame:
        :type frame: tk.Frame
        :param images:
        :type images: SmileyImages
        :param cb: callback function for starting new game
        :type cb:
        """
        self._frame = frame
        self._images: SmileyImages = images
        self._btn = None
        self._cb = cb

        self._thread = None  # todo handle image selection based in new thread

    def init(self):
        """
        initializes smiley button and set image
        :return: None
        :rtype: None
        """
        self._btn = tk.Button(self._frame, bd=0, command=lambda: self._cb())
        self._btn.place(x=0, y=0, width=SMILEY_WIDTH, height=SMILEY_HEIGHT)
        self._btn._image = self._images.smiley_start
        self._btn.configure(image=self._btn._image)

    def set_lost(self):
        """
        set smiley to lost face
        :return: None
        :rtype: None
        """
        self._btn.image = self._images.smiley_lost
        self._btn.configure(image=self._btn.image)

    def set_won(self):
        """
        set smiley to won face
        :return: None
        :rtype: None
        """
        self._btn.image = self._images.smiley_won
        self._btn.configure(image=self._btn.image)

    def set_start(self):
        """
        sets smiley to start face
        :return: None
        :rtype: None
        """
        self._btn.image = self._images.smiley_start
        self._btn.configure(image=self._btn.image)
