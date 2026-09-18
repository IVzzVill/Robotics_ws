# Importa ROS 2 y el tipo de mensaje utilizado por el publicador
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray


class TurtleController(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('turtle_controller')

        # Escucha las lecturas de ambos ejes del joystick
        self.subscription_ = self.create_subscription(
            Int32MultiArray,
            '/joystick/raw',
            self.joystick_callback,
            10
        )

        self.get_logger().info('Esperando datos del joystick')

    def joystick_callback(self, msg):
        # Comprueba que el mensaje contenga exactamente dos valores
        if len(msg.data) != 2:
            self.get_logger().warning('Se esperaban dos valores del joystick')
            return

        # Obtiene las lecturas en el mismo orden que las envía la ESP32
        valor_x = msg.data[0]
        valor_y = msg.data[1]

        # Descarta valores fuera del rango del ADC de 12 bits
        if not (0 <= valor_x <= 4095 and 0 <= valor_y <= 4095):
            self.get_logger().warning('Lectura fuera del rango de 0 a 4095')
            return

        # Muestra los valores recibidos para comprobar la suscripción
        self.get_logger().info(f'Recibido: X = {valor_x}, Y = {valor_y}')


def main(args=None):
    # Inicia ROS 2 y crea el nodo
    rclpy.init(args=args)
    node = TurtleController()

    try:
        # Mantiene el nodo activo para recibir mensajes
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Permite detener el programa con Ctrl+C
        pass
    finally:
        # Libera el nodo y cierra ROS 2
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
