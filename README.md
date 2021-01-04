# py_tk_minesweeper
Copy of WinXP Minesweeper in pythons tkinter.
The original game is already provided inside the repository

### Idea
This project meant to be a programming exercise done to be able to compare different gui frameworks in different languages

For further restrictions a strict object oriented approach was used.

As using as few dependencies as logically possible was part of the challenge only the following built in packages are used

```
os
sys
random
time
threading
logging
```

### Run Minesweeper without Python

For playing without the need to install Python, the executables are provided inside the dist folder.

 * *Minesweeper.exe*
 * *Minesweeper_DEBUG.exe*

The Debug variant does not disable the console and returns a full log printout provided by pyInstaller and the logging module.
For an original experience consider using the non debug variant.

### Run with Python

The code is written in **Python 3.7.8**, which needs to be installed 

This packages have to be installed before running:

```
pip install tkintertable
```


Run the game by calling from console with following command or simply by doubleclicking the *minesweeper.py* file in the root folder.

```
python minesweeper.py
```

##### Debug mode

If the game is called with argument *--debug*, various additional debug options are available.
Hint: Some debug options are not possible if console is deactivated as in the Minesweeper.exe


```
python minesweeper.py --debug
Minesweeper.exe --debug
```

* F3 prints various field size of the main window
* F4 reveals hidden fields without having impact on game functionality (hide again by pressing F4 again to continue playing)


##### Open todos

 * [x] Dynamic Pixel for pixel recreation of the original Windows XP Minesweeper
 * [x] Basic game functionality
 * [x] Change game mode over menu options
 * [ ] Highscore system with json/ini file saving (Can be hard inside .exe file ?!)
 * [ ] Fill remaining menu options inside help Menu
 * [ ] Add game sound
 * [ ] Smiley reactions for click actions by binding *ButtonPress*, *ButtonRelease*
