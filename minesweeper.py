

import gui
import classes


DEBUG = False  # todo implement debug mode in sys args


# todo am ende aufräumen und unbenutzte variablen aufräumen/löschen
# todo alles was nicht notwendig ist nicht als klassenvariabe machen
# todo bug fixen mit eins breiter als gedacht
# todo rand field frame schöner machen, gleicht nicht genau dem original


if __name__ == '__main__':

    print("Starting game: ")

    game = classes.Game()
    mw = gui.MinesweeperGUI(game)
    mw.build_gui()

    print("Done ...")