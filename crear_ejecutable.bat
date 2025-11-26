@echo off
echo creando ejecutable...
pyinstaller --onefile --windowed --add-data "Metro.png;." MetroApp.py

:: onefile : crea el ejecutable como unico archivo en vez de un ejecutable dentro de una carpeta
:: windowed : evita que se abra el terminal al ejecutar el .exe
:: add-data : adjunta la imagen al proyecto

pause