#!/usr/bin/python3.7
# -*- coding: utf-8 -*-


import tkinter as tk
import os
import sys
import logging


# logging module
LOG_LEVEL = logging.DEBUG

LOG = logging.getLogger()
LOG.setLevel(LOG_LEVEL)
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
sh = logging.StreamHandler()
sh.setLevel(LOG_LEVEL)
sh.setFormatter(formatter)
LOG.addHandler(sh)


def handle_excep(exception, with_tb=True):
    """ prints exception """
    LOG.critical(exception)
    if with_tb:
        import traceback
        LOG.critical(traceback.format_exc())


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_img(rel_path):
    """
    return PhotoImage of image in path, uses resource path for pyInstaller
    :param rel_path:
    :type rel_path: path
    :return: loaded image for tkinter usage
    :rtype: tk.PhotoImage
    """
    return tk.PhotoImage(file=resource_path(rel_path))


def check_pyversion(designed_for):
    """ prints warning if not expected python version"""
    if str(sys.version_info[0]) + '.' + str(sys.version_info[1]) != designed_for:
        print("SYSTEM INFO: Designed for Python Version '{}' and you have {}.{}. Program might crash!".format(designed_for, sys.version_info[0], sys.version_info[1]))


def get_logger(name, level=LOG_LEVEL):
    """
    creates logger class linked to root logger
    :param name:
    :type name: str
    :param level:
    :type level:
    :return:
    :rtype:
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
