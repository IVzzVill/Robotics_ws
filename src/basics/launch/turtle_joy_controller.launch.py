# Importa la descripción del lanzamiento y la acción para iniciar nodos
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Inicia los tres nodos del control con joystick
    return LaunchDescription([
        # Abre el simulador de la tortuga
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            output='screen'
        ),

        # Recibe las lecturas y publica las velocidades de la tortuga
        Node(
            package='basics',
            executable='turtle_controller',
            output='screen'
        ),

        # Lee la ESP32 y publica los dos valores del joystick
        Node(
            package='basics',
            executable='joystick_publisher',
            output='screen'
        ),
    ])
