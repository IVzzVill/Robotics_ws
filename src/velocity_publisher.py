# Importación de herramientas para trabajar con nodos de ROS 2
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class VelocityPublisher(Node):

    def __init__(self):
	# Asigno el nombre con el que ROS identifica el nodo
        super().__init__('velocity_publisher')
	
	# Creacion de un publicador de números en el tópico /velocity
        # Se conservan hasta 10 mensajes en el historial
        self.publisher_ = self.create_publisher(Float32,'/velocity',10)
	# Se inicia el valor de velocidad en cero
        self.Vel = 0.0
	# Ejecuta la publicación cada medio segundo
        self.timer_ = self.create_timer(0.5,
            self.publish_velocity
        )

    def publish_velocity(self):
	# Guarda la velocidad actual en el mensaje y lo envia
        msg = Float32()

        msg.data = self.Vel

        self.publisher_.publish(msg)
	# Muestra en la terminal el valor que se publico
        self.get_logger().info(
            f'Vel = {self.Vel:.1f}'
        )
	# Aumenta la velocidad hasta 1.5 y después reinicia el ciclo
        if self.Vel < 1.5:
            self.Vel = round(self.Vel + 0.1, 1)
        else:
            self.Vel = 0.0


def main(args=None):
    # Inicia ROS 2 y crea el publicador
    rclpy.init(args=args)
   # Crea el nodo publicador
    node = VelocityPublisher()
   # Se mantiene el nodo activo para ejecutar el temporizador
    rclpy.spin(node)
   #Libera recursos del nodo
    node.destroy_node()
    #cierre de comunicacion con ROS2
    rclpy.shutdown()


if __name__ == '__main__':
    main()
