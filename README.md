Instrucciones de ejecución archivo MetroApp.exe:

El ejecutable se ha creado usando el comando incluido en el archivo crear_ejecutable.bat:

pyinstaller --onefile --windowed --add-data "Metro.png;." MetroApp.py

El ejecutable se encuentra, y pyinstaller lo crea dentro de la carpeta dist del proyecto.
Gracias ha usar la opción - -onefile el ejecutable se puede ejecutar desde cualquier carpeta tan solo dándole doble click.
Para crear el ejecutable es necesario tener instalado en el equipo la siguiente librería:

pyinstaller

Comando de instalación de la librería:
pip install pyinstaller

Instrucciones de ejecución MetroApp.py:

Para ejecutar la aplicación desde el archivo de python es necesario tener instalado en el equipo las siguientes librerías no estándar de python:

networkx
tkinter
PIL

Comandos de instalación de las librerías:

pip3 install networkx
pip install tkinter
pip install Pillow

También utilizamos las siguientes librerías estandar:

datetime
sys, os
re

