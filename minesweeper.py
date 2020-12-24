

import gui
import classes


DEBUG = False  # todo implement debug mode in sys args


AVAILABLE_MODES = {  # todo different game settings: Beginner, Intermidiate, ...
    'Beginner': classes.GameSetting(rows=9, cols=9, bombs=10),
    'Intermediate': classes.GameSetting(rows=16, cols=16, bombs=40),
    'Expert': classes.GameSetting(rows=16, cols=30, bombs=99),
    'Custom': classes.GameSetting(rows=None, cols=None, bombs=None)  # todo
}

# todo am ende aufräumen und unbenutzte variablen aufräumen/löschen
# todo alles was nicht notwendig ist nicht als klassenvariabe machen
# todo bug fixen mit eins breiter als gedacht
# todo rand field frame schöner machen, gleicht nicht genau dem original


if __name__ == '__main__':


    print("Starting game: ")

    mw = gui.MinesweeperGUI()
    mw.build_gui(game_setting=AVAILABLE_MODES['Intermediate'])

    print("Done ...")