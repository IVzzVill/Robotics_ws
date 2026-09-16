# Importa la comunicación serial y las funciones de tiempo
import serial
import time

# Define el puerto y la velocidad de comunicación
PORT = '/dev/ttyUSB0'
BAUDRATE = 115200

# Abre la conexión con la ESP32
esp32 = serial.Serial(PORT, BAUDRATE, timeout=1)

# Espera dos segundos para permitir que la placa se prepare
time.sleep(2)

while True:
    # Solicita una orden desde el teclado
    dato = input("Escribe 1 para encender, 0 para apagar, q para salir: ")

    # Envía la orden de encendido
    if dato == '1':
        esp32.write(b'1\n')

    # Envía la orden de apagado
    elif dato == '0':
        esp32.write(b'0\n')

    # Termina el ciclo cuando se escribe q
    elif dato == 'q':
        break

# Cierra el puerto después de salir del ciclo
esp32.close()
