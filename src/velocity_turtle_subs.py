# Importa ROS 2 y el mismo tipo de mensaje que usa el publicador
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocitySubscriber(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('velocity_turtle_subs')

        # Escucha el tópico de movimiento de la tortuga
        # Ejecuta velocity_callback cuando recibe un mensaje Twist
        self.subscription_ = self.create_subscription(Twist,'/turtle1/cmd_vel',self.velocity_callback,10)

    def velocity_callback(self, msg):
        # Obtiene la velocidad translacional del mensaje
        Velocity = msg.linear.x

        # Muestra la velocidad enviada con un decimal
        self.get_logger().info(f'Vel = {Velocity:.1f} m/s')


def main(args=None):
    # Inicia ROS 2
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
