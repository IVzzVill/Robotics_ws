# Importa ROS 2 y el mensaje para controlar la velocidad de la tortuga
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VelocityPublisher(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('velocity_turtle_pub')

        # Crea el publicador en el tópico de movimiento de la tortuga
        self.publisher_ = self.create_publisher(Twist,'/turtle1/cmd_vel',10)

        # Inicia la velocidad en cero y registra si terminó el incremento
        self.Vel = 0.0
        self.detenida = False

        # Ejecuta la publicación cada medio segundo
        self.timer_ = self.create_timer(0.5,self.publish_velocity)

    def publish_velocity(self):
        # Mantiene la velocidad en cero después de terminar el incremento
        if self.detenida:
            self.Vel = 0.0

        # Asigna la velocidad translacional sin agregar giro
        msg = Twist()
        msg.linear.x = self.Vel
        msg.angular.z = 0.0

        # Publica la velocidad y muestra el valor enviado
        self.publisher_.publish(msg)
        self.get_logger().info(f'Vel = {self.Vel:.1f} m/s')

        # Incrementa la velocidad hasta publicar 1.2
        # Activa la detención para la siguiente publicación
        if not self.detenida:
            if self.Vel < 1.2:
                self.Vel = round(self.Vel + 0.1, 1)
            else:
                self.detenida = True


def main(args=None):
    # Inicia ROS 2
    rclpy.init(args=args)

    # Crea el nodo publicador
    node = VelocityPublisher()

    # Mantiene el nodo activo para ejecutar el temporizador
    rclpy.spin(node)

    # Libera los recursos del nodo
    node.destroy_node()

    # Cierra la comunicación con ROS 2
    rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
