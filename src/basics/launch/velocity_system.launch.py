# Importa la descripción del lanzamiento y la acción para iniciar nodos
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Define los dos nodos que se ejecutan con este launch
    return LaunchDescription([
        # Inicia el publicador y muestra su salida en la terminal
        Node(
            package='basics',
            executable='velocity_publisher',
            output='screen'
        ),

        # Inicia el suscriptor y muestra su salida en la misma terminal
        Node(
            package='basics',
            executable='velocity_subscriber',
            output='screen'
        ),
    ])
