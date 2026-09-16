# Importa ROS 2 y el mensaje entero para enviar el estado del LED
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class LedBlink(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('led_blink')

        # Crea el publicador del estado del LED
        self.publisher_ = self.create_publisher(Int32, '/led_command', 10)

        # Inicia el estado en encendido
        self.estado = 1

        # Cambia el estado cada segundo
        self.timer_ = self.create_timer(1.0, self.blink_callback)
        self.get_logger().info('Nodo iniciado')

        # Publica el estado inicial
        self.publicar_estado()

    def blink_callback(self):
        # Alterna entre encendido y apagado
        if self.estado == 1:
            self.estado = 0
        else:
            self.estado = 1

        # Envía el nuevo estado
        self.publicar_estado()

    def publicar_estado(self):
        # Guarda el estado en un mensaje Int32
        msg = Int32()
        msg.data = self.estado

        # Publica el mensaje y muestra el estado en la terminal
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: {self.estado}')


def main(args=None):
    # Inicia ROS 2 y crea el nodo
    rclpy.init(args=args)
    node = LedBlink()

    # Mantiene el nodo activo para ejecutar el temporizador
    rclpy.spin(node)

    # Libera el nodo y cierra ROS 2
    node.destroy_node()
    rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
