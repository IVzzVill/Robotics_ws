# Importa la biblioteca de comunicación serial
import serial

# Define el puerto y la velocidad de comunicación
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200

# Abre la conexión con la ESP32
esp32 = serial.Serial(PORT, BAUDRATE, timeout=1)

# Mantiene la lectura del puerto de forma continua
while True:
    # Lee una línea y elimina los espacios y el salto de línea
    linea = esp32.readline().decode().strip()

    # Muestra la lectura cuando la línea no está vacía
    if linea:
        print(f'ADC = {linea}')
