@echo off
echo creando ejecutable...
pyinstaller --onefile --windowed --add-data "Metro.png;." MetroApp.py

pause