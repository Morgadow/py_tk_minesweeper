

import time
import tkinter as tk
import threading

from constants import *
from classes import Size
import utils


class CounterImages(object):
    """
    all possible images for counter fields for faster image setting
    """

    Cnt_minus = None
    Cnt_0 = None
    Cnt_1 = None
    Cnt_2 = None
    Cnt_3 = None
    Cnt_4 = None
    Cnt_5 = None
    Cnt_6 = None
    Cnt_7 = None
    Cnt_8 = None
    Cnt_9 = None

    def __init__(self):

        self.Cnt_minus = utils.get_img('ui\\counter\\-.png')
        self.Cnt_0 = utils.get_img('ui\\counter\\0.png')
        self.Cnt_1 = utils.get_img('ui\\counter\\1.png')
        self.Cnt_2 = utils.get_img('ui\\counter\\2.png')
        self.Cnt_3 = utils.get_img('ui\\counter\\3.png')
        self.Cnt_4 = utils.get_img('ui\\counter\\4.png')
        self.Cnt_5 = utils.get_img('ui\\counter\\5.png')
        self.Cnt_6 = utils.get_img('ui\\counter\\6.png')
        self.Cnt_7 = utils.get_img('ui\\counter\\7.png')
        self.Cnt_8 = utils.get_img('ui\\counter\\8.png')
        self.Cnt_9 = utils.get_img('ui\\counter\\9.png')


class CounterBaseClass(object):

    size = Size(height=COUNTER_HEIGHT, width=COUNTER_WIDTH * 3)

    def __init__(self, frame, start, images):
        """
        constructor for counter base class
        :param frame: gui frame to place counter images inside
        :type frame: tk.Frame
        :param start: start index
        :type start: int
        :param images: all possible images
        :type images: CounterImages
        """

        self.count = start
        self._start = start

        self._logger = utils.get_logger(self.__class__.__name__)
        self._frame = frame
        self._images = images
        self._str_to_image = {
                '-': self._images.Cnt_minus,
                '0': self._images.Cnt_0,
                '1': self._images.Cnt_1,
                '2': self._images.Cnt_2,
                '3': self._images.Cnt_3,
                '4': self._images.Cnt_4,
                '5': self._images.Cnt_5,
                '6': self._images.Cnt_6,
                '7': self._images.Cnt_7,
                '8': self._images.Cnt_8,
                '9': self._images.Cnt_9
            }
        self._labels = [None] * 3

        self._is_counting = False  # flag for counting flag
        self._thread = None

    def init(self):
        """
        initialize labels and place first images
        :return:
        :rtype:
        """
        for i in range(len(self._labels)):
            self._labels[i] = tk.Label(self._frame)
            self._labels[i].place(x=COUNTER_WIDTH * i, y=0, width=COUNTER_WIDTH, height=COUNTER_HEIGHT)
            self._labels[i].cnt = 0
            self._labels[i].image = None

        self.update_img()
        self._logger.debug("Created counter elements")

    def count_up(self):
        """
        adds one to counter and updates picture
        :return: None
        :rtype: None
        """
        if self.count < 999:
            self.count += 1
            self.update_img()

    def reduce_one(self):
        """
        reduces count by one and updates picture
        :return: None
        :rtype: None
        """
        self.count -= 1
        self.update_img()

    def update_img(self):
        """
        set image based on self.count
        :return: None
        :rtype: None
        """
        if self.count >= 0:
            new_rep = '0' * (3 - len(str(self.count)))
            new_rep += str(self.count)[-max(len(str(self.count)), 3):]
        else:
            new_rep = '-' + '0' * (2 - len(str(self.count)))
            new_rep += str(self.count)[-max(len(str(self.count)), 2):]

        for index, elem in enumerate(new_rep):
            if elem != self._labels[index].cnt:
                self._labels[index].cnt = elem
                self._labels[index].image = self._str_to_image[elem]
                self._labels[index].configure(image=self._labels[index].image)

        self._logger.debug("Set number '{}' to counter".format(new_rep))

    def reset(self, start=None):
        """
        resets game counter to start value
        :param start:
        :type start: int or None
        :return: None
        :rtype: None
        """
        self.count = (self._start if start is None else start)
        self.update_img()


class TimeCounter(CounterBaseClass):
    """
    counter class for game time
    """

    @property
    def is_counting(self):
        """
        property getter of is counting flag
        :return:
        :rtype: bool
        """
        return self._is_counting

    @is_counting.setter
    def is_counting(self, status):
        """
        property setter of is counting flag, starts and stops counter
        :param status:
        :type status: bool
        :return: None
        :rtype: None
        """
        if not status and self._is_counting:
            self.stop_timer()
        if status and self._is_counting:
            self.start_timer()

    def start_timer(self):
        """
        starts game timer and keep it updated
        :return: None
        :rtype: None
        """
        if not self._is_counting:
            self._is_counting = True
            self._thread = threading.Thread(name='GameTimeCounter', target=self._count, daemon=True)
            self._thread.start()
            self._logger.debug("Started counting game counter")

    def stop_timer(self):
        """
        stop counting timer
        :return: None
        :rtype: None
        """
        self._is_counting = False
        self._thread.join()

    def _count(self):
        """
        auxiliary function for counting thread
        :return:
        :rtype:
        """
        while self._is_counting:
            time.sleep(1)
            self.count_up()
        self._logger.debug("Stopped counting game counter")

    def reset(self, start=None):
        """
        resets game counter to start value
        :param start:
        :type start: int or None
        :return: None
        :rtype: None
        """
        self.stop_timer()
        self.count = (self._start if start is None else start)
        self.update_img()


class FlagCounter(CounterBaseClass):

    pass
