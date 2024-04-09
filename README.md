# PROYECTO C3 SII-FT -- COINMARU PREVIEW VERSION

Coinmaru Preview es una aplicación de escritorio que escanea, clasifica y suma monedas de México. Sin embargo, en un futuro se planea integrar monedas de otros países más allá de México, incluyendo Japón, Estados Unidos, Canadá y Perú, esta ya siendo la versión completa de Coinmaru.

## Cómo preparar la aplicación para correr
### Todos dispositivos
- Install Python
- Install pip
- Run this command: `pip install venv` # Descarga el agente del entorno virtual
- Run this command: `py -m venv venv`  # Crea el entorno virtual

### Windows
- Run this command: `cd venv/Scripts` # Se entra al entorno virtual
- Run this command: `activate` # Se activa el entorno virtual
- Run this command: `cd .. && cd ..` # Se vuelve a la ruta original
- Run this command: `pip install -r requirements.txt` # Se descargan las dependencias dentro del entorno virtual
### Linux
- Run this command: `source venv/bin/activate` # Se entra al entorno virtual
- Run this command: `pip install -r requirements.txt` # Se descargan las dependencias dentro del entorno virtual

## Cómo correr
- Run `py main.py`
