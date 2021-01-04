@echo off & setlocal

pyinstaller --name Minesweeper^
   --paths "%cd%"^
   --onefile ^
   --noconsole ^
   --clean ^
   --add-data "%cd%/ui";"." ^
   --add-data "%cd%/ui/icon.ico";"./ui" ^
   --add-data "%cd%/ui/counter";"./ui" ^
   --add-data "%cd%/ui/smiley";"./ui" ^
   --add-data "%cd%/ui/fields";"./ui" ^
   --add-data "%cd%/ui/fields/front";"./ui/fields" ^
   --add-data "%cd%/ui/fields/back";"./ui/fields" ^
   --add-data "%cd%/ui/counter/*.png";"./ui/counter" ^
   --add-data "%cd%/ui/smiley/*.png";"./ui/smiley" ^
   --add-data "%cd%/ui/fields/front/*.png";"./ui/fields/front" ^
   --add-data "%cd%/ui/fields/back/*.png";"./ui/fields/back" ^
   --icon "%cd%/ui/icon.ico" ^
   ./minesweeper.py
   
   
 pyinstaller --name Minesweeper_DEBUG^
   --paths "%cd%"^
   --onefile ^
   --clean ^
   --debug=all ^
   --add-data "%cd%/ui";"." ^
   --add-data "%cd%/ui/icon.ico";"./ui" ^
   --add-data "%cd%/ui/counter";"./ui" ^
   --add-data "%cd%/ui/smiley";"./ui" ^
   --add-data "%cd%/ui/fields";"./ui" ^
   --add-data "%cd%/ui/fields/front";"./ui/fields" ^
   --add-data "%cd%/ui/fields/back";"./ui/fields" ^
   --add-data "%cd%/ui/counter/*.png";"./ui/counter" ^
   --add-data "%cd%/ui/smiley/*.png";"./ui/smiley" ^
   --add-data "%cd%/ui/fields/front/*.png";"./ui/fields/front" ^
   --add-data "%cd%/ui/fields/back/*.png";"./ui/fields/back" ^
   --icon "%cd%/ui/icon.ico" ^
   ./minesweeper.py
   
   
   
   
RMDIR /S /Q %cd%\build
RMDIR /S /Q %cd%\__pycache__
RMDIR /S /Q %cd%\.idea
del %cd%\Minesweeper.spec
del %cd%\Minesweeper_DEBUG.spec