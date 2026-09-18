# Importa ROS 2, el mensaje para enviar ambos ejes y la comunicación serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
import serial


class JoystickPublisher(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('joystick_publisher')

        # Crea el publicador de las lecturas del joystick
        self.publisher_ = self.create_publisher(
            Int32MultiArray, '/joystick/raw', 10
        )

        # Abre el puerto de la ESP32 sin bloquear la lectura
        self.serial_ = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)

        # Guarda los bytes hasta recibir una línea completa
        self.buffer_ = bytearray()

        # Revisa el puerto cada 0.01 segundos
        self.timer_ = self.create_timer(0.01, self.read_serial)
        self.get_logger().info('Esperando lecturas del joystick')

    def read_serial(self):
        # Obtiene la cantidad de bytes disponibles
        disponibles = self.serial_.in_waiting
        if disponibles == 0:
            return

        # Agrega los datos recibidos al contenido pendiente
        self.buffer_.extend(self.serial_.read(disponibles))

        # Procesa únicamente las líneas completas
        while b'\n' in self.buffer_:
            linea, _, resto = self.buffer_.partition(b'\n')
            self.buffer_ = bytearray(resto)

            try:
                # Separa los dos valores enviados como X,Y
                partes = linea.decode('ascii').strip().split(',')
                if len(partes) != 2:
                    continue

                valor_x = int(partes[0])
                valor_y = int(partes[1])
            except (UnicodeDecodeError, ValueError):
                # Descarta mensajes de inicio o datos que no sean números
                continue

            # Comprueba que las lecturas estén dentro del rango de 12 bits
            if not (0 <= valor_x <= 4095 and 0 <= valor_y <= 4095):
                continue

            # Publica primero el eje X y después el eje Y
            msg = Int32MultiArray()
            msg.data = [valor_x, valor_y]
            self.publisher_.publish(msg)

            # Muestra las lecturas para comprobar la comunicación
            self.get_logger().info(f'X = {valor_x}, Y = {valor_y}')

        # Descarta datos acumulados si no llegan saltos de línea válidos
        if len(self.buffer_) > 4096:
            self.buffer_.clear()


def main(args=None):
    # Inicia ROS 2 y crea el nodo
    rclpy.init(args=args)
    node = None

    try:
        node = JoystickPublisher()

        # Mantiene el nodo activo para recibir y publicar lecturas
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Permite detener el programa con Ctrl+C
        pass
    finally:
        # Cierra el puerto y libera los recursos
        if node is not None:
            node.serial_.close()
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
