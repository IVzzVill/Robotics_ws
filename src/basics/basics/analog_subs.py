# Importa ROS 2 y el mensaje entero utilizado por el publicador
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class AnalogSubscriber(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('analog_subscriber')

        # Escucha /analog y ejecuta analog_callback al recibir un mensaje
        self.subscription_ = self.create_subscription(Int32, '/analog', self.analog_callback, 10)
        self.get_logger().info('Esperando datos')

    def analog_callback(self, msg):
        # Obtiene la lectura del campo data
        valor = msg.data

        # Muestra el valor del ADC en la terminal
        self.get_logger().info(f'ADC = {valor}')


def main(args=None):
    # Inicia ROS 2 y crea el suscriptor
    rclpy.init(args=args)
    node = AnalogSubscriber()

    # Mantiene el nodo activo para recibir mensajes
    rclpy.spin(node)

    # Libera el nodo y cierra ROS 2
    node.destroy_node()
    rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
