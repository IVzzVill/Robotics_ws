# Importa ROS 2, el mensaje entero y la comunicación serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial


class AnalogSerialPublisher(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('analog_serial_pub')

        # Crea el publicador de lecturas en el tópico /analog
        self.publisher_ = self.create_publisher(Int32,'/analog', 10)

        # Abre la conexión con la ESP32 a 115200 baudios
        self.serial_ = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        # Programa la revisión del puerto cada 0.01 segundos
        self.timer_ = self.create_timer(0.01, self.read_serial)
        self.get_logger().info('ESP32 conectada')

    def read_serial(self):
        # Comprueba si hay bytes disponibles en el puerto
        if self.serial_.in_waiting > 0:
            # Lee una línea y elimina los espacios y el salto de línea
            linea = self.serial_.readline().decode().strip()

            # Comprueba que la línea contenga únicamente dígitos
            if linea.isdigit():
                # Convierte la lectura a entero y la guarda en el mensaje
                valor = int(linea)
                msg = Int32()
                msg.data = valor

                # Publica la lectura recibida de la ESP32
                self.publisher_.publish(msg)


def main(args=None):
    # Inicia ROS 2 y crea el nodo
    rclpy.init(args=args)
    node = AnalogSerialPublisher()

    # Mantiene el nodo activo para revisar el puerto serial
    rclpy.spin(node)

    # Cierra el puerto y libera los recursos al llegar a estas instrucciones
    node.serial_.close()
    node.destroy_node()
    rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
