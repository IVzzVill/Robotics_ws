# Importa ROS 2 y el mismo tipo de mensaje que usa el publicador
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class VelocitySubscriber(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('velocity_subscriber')

        # Crea la suscripción al tópico /velocity con mensajes Float32
        # Ejecuta velocity_callback cuando recibe un mensaje
        # Conserva hasta 10 mensajes en el historial
        self.subscription_ = self.create_subscription(Float32,'/velocity',self.velocity_callback,10)

    def velocity_callback(self, msg):
        # Obtiene la velocidad del mensaje recibido
        Velocity = msg.data

        # Muestra la velocidad con un decimal en metros por segundo
        self.get_logger().info(f'Vel = {Velocity:.1f} m/s')


def main(args = None):
    # Inicia la comunicación con ROS 2
    rclpy.init(args=args)

    # Crea el nodo suscriptor
    node = VelocitySubscriber()

    # Mantiene el nodo activo para recibir mensajes
    rclpy.spin(node)

    # Libera los recursos del nodo
    node.destroy_node()

    # Cierra la comunicación con ROS 2
    rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
