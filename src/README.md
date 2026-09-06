# Publicador y suscriptor de velocidad en ROS 2

**Alumno:** Ivan Vazquez Villar

## Descripción de la actividad

La práctica consiste en ejecutar dos nodos de ROS 2 en terminales diferentes para enviar y recibir datos mediante el tópico /velocity.

Se utilizó ROS 2 Jazzy y Python con la biblioteca rclpy.

## Funcionamiento del publicador

El archivo velocity_publisher.py crea el nodo velocity_publisher y un publicador en el tópico /velocity utilizando mensajes std_msgs/msg/Float32.

Un temporizador ejecuta la función publish_velocity cada 0.5 segundos, equivalente a una frecuencia configurada de 2 Hz. La función coloca la velocidad en el campo data del mensaje y lo publica.

El valor comienza en 0.0, aumenta en pasos de 0.1 hasta 1.5 y después vuelve a 0.0 para repetir el ciclo.

## Funcionamiento del suscriptor

El archivo velocity_subscriber.py crea el nodo velocity_subscriber y una suscripción al tópico /velocity con el mismo tipo de mensaje Float32.

Cada vez que recibe un mensaje, ejecuta velocity_callback. Esta función obtiene el valor de msg.data y lo muestra en la terminal con un decimal y la etiqueta m/s.

Float32 transporta únicamente el número. La unidad m/s es la interpretación utilizada en esta práctica.

Ambos nodos utilizan una profundidad de historial de 10 mensajes.

## Estructura del repositorio

```text
Robotics_ws/
└── src/
    ├── README.md
    ├── velocity_publisher.py
    └── velocity_subscriber.py
```

## Ejecución

El repositorio local se encuentra en ~/robotics_ws.

Los programas se ejecutan directamente con Python, por lo que esta estructura no requiere colcon build. Es necesario cargar el entorno de ROS 2 en cada terminal.

### Terminal 1: publicador

```bash
source /opt/ros/jazzy/setup.bash
cd ~/robotics_ws
python3 src/velocity_publisher.py
```

### Terminal 2: suscriptor

```bash
source /opt/ros/jazzy/setup.bash
cd ~/robotics_ws
python3 src/velocity_subscriber.py
```

Los dos programas deben permanecer ejecutándose simultáneamente. Para detenerlos se utiliza Ctrl+C en cada terminal.

## Comprobación del funcionamiento

En una tercera terminal se carga el entorno:

```bash
source /opt/ros/jazzy/setup.bash
```

### Revisión de nodos

```bash
ros2 node list
ros2 node info /velocity_publisher
ros2 node info /velocity_subscriber
```

Estos comandos permiten identificar los nodos activos y revisar sus publicaciones y suscripciones.

### Revisión del tópico

```bash
ros2 topic list
ros2 topic info /velocity
```

El tópico /velocity utiliza std_msgs/msg/Float32. Con únicamente los dos programas activos, corresponde un publicador y un suscriptor.

### Visualización de datos

```bash
ros2 topic echo /velocity
```

Muestra los valores del campo data. Se detiene con Ctrl+C antes de continuar.

### Revisión de frecuencia

```bash
ros2 topic hz /velocity
```

Mide la frecuencia de recepción, que debe aproximarse a 2 Hz según el temporizador configurado. Se detiene con Ctrl+C.

Los comandos echo y hz crean suscripciones adicionales mientras están ejecutándose.

### Grafo de ROS

```bash
ros2 run rqt_graph rqt_graph
```

El grafo permite visualizar la conexión:

```text
/velocity_publisher → /velocity → /velocity_subscriber
```

Durante la ejecución se comprobó que el suscriptor mostraba los valores enviados por el publicador y que el ciclo continuaba después de regresar a cero.

## Problemas encontrados y soluciones

### Tipo de dato al reiniciar la velocidad

El publicador se detenía después de publicar 1.5 porque el reinicio asignaba el entero 0. Se cambió a 0.0 para mantener un valor flotante compatible con Float32.

### Mezcla de tabulaciones y espacios

El suscriptor presentó un TabError por mezclar tabulaciones y espacios. Se corrigió la sangría utilizando espacios de forma consistente.

### Suscripción fuera del constructor

La línea self.subscription_ quedó fuera de __init__ debido a la sangría y produjo el error NameError: name 'self' is not defined. Se colocó dentro del constructor, al mismo nivel que super().__init__.

### Autenticación en GitHub

GitHub rechazó la contraseña de la cuenta al intentar subir los cambios mediante HTTPS. Se utilizó un token de acceso con permiso de escritura de contenido para el repositorio.

## Control de versiones

El desarrollo se organizó en tres etapas:

1. Commit inicial con el trabajo realizado en clase
2. Segundo commit al comprobar el funcionamiento del suscriptor
3. Commit final con la documentación y el enlace a la evidencia

## Evidencia en video

[Ver video de la práctica](https://drive.google.com/file/d/1HbDn0eetMj2WAF0Cv_EMog6rGpy6UaAj/view?usp=sharing)
