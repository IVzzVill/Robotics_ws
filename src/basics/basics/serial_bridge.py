# Importa ROS 2, el mensaje entero y la comunicación serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial


class SerialBridge(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('serial_bridge')

        # Escucha las órdenes publicadas en /led_command
        self.subscription_ = self.create_subscription(Int32, '/led_command', self.led_callback,10)

        # Abre el puerto de la ESP32 a 115200 baudios
        self.serial_ = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        self.get_logger().info('Esperando mensajes')

    def led_callback(self, msg):
        # Envía el carácter 1 y un salto de línea para encender el LED
        if msg.data == 1:
            self.serial_.write(b'1\n')
            self.get_logger().info('ROS 2 -> Serial: 1')

        # Envía el carácter 0 y un salto de línea para apagar el LED
        elif msg.data == 0:
            self.serial_.write(b'0\n')
            self.get_logger().info('ROS 2 -> Serial: 0')


def main(args=None):
    # Inicia ROS 2 y crea el puente serial
    rclpy.init(args=args)
    node = SerialBridge()

    # Mantiene el nodo activo para recibir mensajes
    rclpy.spin(node)

    # Cierra el puerto y libera los recursos al llegar a estas instrucciones
    node.serial_.close()
    node.destroy_node()
    rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
