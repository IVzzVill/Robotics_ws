# Importa ROS 2, las lecturas del joystick y el mensaje de velocidad
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist
import time


class TurtleController(Node):
    def __init__(self):
        # Asigna el nombre del nodo
        super().__init__('turtle_controller')

        # Define los centros medidos y la tolerancia inicial
        self.centro_x = 1835
        self.centro_y = 1765
        self.zona_muerta = 100

        # Define los límites iniciales de velocidad
        self.max_lineal = 1.5
        self.max_angular = 1.5

        # Guarda las velocidades y el momento del último mensaje válido
        self.lineal = 0.0
        self.angular = 0.0
        self.ultima_lectura = None

        # Publica las órdenes de movimiento para la tortuga
        self.publisher_ = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10
        )

        # Recibe las lecturas del publicador serial
        self.subscription_ = self.create_subscription(
            Int32MultiArray,
            '/joystick/raw',
            self.joystick_callback,
            10
        )

        # Envía las velocidades cada 0.05 segundos
        self.timer_ = self.create_timer(0.05, self.publish_velocity)
        self.get_logger().info('Controlador de la tortuga iniciado')

    def normalizar(self, valor, centro):
        # Calcula cuánto se separa la lectura de su centro
        diferencia = valor - centro

        # Mantiene cero dentro de la zona muerta
        if abs(diferencia) <= self.zona_muerta:
            return 0.0

        # Escala cada lado según el recorrido disponible hasta su extremo
        if diferencia > 0:
            resultado = (
                (diferencia - self.zona_muerta)
                / (4095 - centro - self.zona_muerta)
            )
        else:
            resultado = (
                (diferencia + self.zona_muerta)
                / (centro - self.zona_muerta)
            )

        # Limita el resultado al intervalo de menos uno a uno
        return max(-1.0, min(1.0, resultado))

    def joystick_callback(self, msg):
        # Comprueba que lleguen dos valores válidos de 12 bits
        if len(msg.data) != 2:
            return

        valor_x = msg.data[0]
        valor_y = msg.data[1]

        if not (0 <= valor_x <= 4095 and 0 <= valor_y <= 4095):
            return

        # Invierte el primer eje para que adelante produzca avance
        self.lineal = (
            -self.normalizar(valor_x, self.centro_x) * self.max_lineal
        )

        # Convierte el segundo eje en giro positivo hacia la izquierda
        self.angular = (
            self.normalizar(valor_y, self.centro_y) * self.max_angular
        )

        # Registra el momento de recepción del mensaje válido
        self.ultima_lectura = time.monotonic()

        # Muestra las lecturas y las velocidades calculadas
        self.get_logger().info(
            f'X = {valor_x}, Y = {valor_y} | '
            f'Lineal = {self.lineal:.2f}, Angular = {self.angular:.2f}'
        )

    def publish_velocity(self):
        # Crea una orden con todas las velocidades en cero
        msg = Twist()

        # Usa las velocidades calculadas solo si hay datos recientes
        if (
            self.ultima_lectura is not None
            and time.monotonic() - self.ultima_lectura <= 0.5
        ):
            msg.linear.x = self.lineal
            msg.angular.z = self.angular

        # Detiene la tortuga si pasan más de 0.5 segundos sin datos válidos
        self.publisher_.publish(msg)


def main(args=None):
    # Inicia ROS 2 y crea el controlador
    rclpy.init(args=args)
    node = TurtleController()

    try:
        # Mantiene el nodo activo
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Permite detener el programa con Ctrl+C
        pass
    finally:
        # Intenta enviar una orden de parada antes de cerrar
        if rclpy.ok():
            node.publisher_.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


# Ejecuta main cuando inicia el archivo directamente
if __name__ == '__main__':
    main()
