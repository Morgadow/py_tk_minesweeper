

import gui
from classes import GameSetting, Game


DEBUG = False  # todo implement debug mode in sys args -> bind sys


# todo am ende aufräumen und unbenutzte variablen aufräumen/löschen
# todo alles was nicht notwendig ist nicht als klassenvariabe machen
# todo constants auflösen und überall unterbringen


AVAILABLE_MODES = {  # todo different game settings: Beginner, Intermediate, ...
    'Beginner': GameSetting(rows=9, cols=9, bombs=10),
    'Intermediate': GameSetting(rows=16, cols=16, bombs=40),
    'Expert': GameSetting(rows=16, cols=30, bombs=99),
    'Custom': GameSetting(rows=None, cols=None, bombs=None)  # todo
}


if __name__ == '__main__':

    print("Starting game: ")

    # game = Game(settings=AVAILABLE_MODES['Beginner'])
    # game = Game(settings=AVAILABLE_MODES['Expert'])
    game = Game()
    mw = gui.MinesweeperGUI(game)
    mw.build_gui()

    print("Done ...")