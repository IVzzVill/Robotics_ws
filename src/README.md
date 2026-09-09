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

Los programas se ejecutan directamente con Python, por lo que esta estructura no requiere colcon build. Es necesario cargar el entorno de ROS 2 en cada terminal en caso de no haberlo hecho antes en el .bashrc

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


---

# Actividad 2: Control de velocidad de una tortuga

## Descripción

En esta actividad se realizaron copias del publicador y del suscriptor de la primera práctica para controlar una tortuga en turtlesim.

La velocidad translacional comienza en 0.0 y aumenta 0.1 cada medio segundo hasta publicar 1.2. En la siguiente publicación se envía 0.0 y se mantiene la tortuga detenida.

## Modificaciones realizadas

Se crearon los archivos velocity_turtle_pub.py y velocity_turtle_subs.py a partir de los programas originales.

Se cambió el mensaje Float32 por geometry_msgs/msg/Twist y el tópico /velocity por /turtle1/cmd_vel, que recibe las órdenes de movimiento de turtlesim.

En el publicador se utiliza msg.linear.x para asignar la velocidad translacional y se mantiene msg.angular.z en cero para avanzar sin girar.

También se agregó una variable llamada detenida para evitar que el incremento vuelva a comenzar después de llegar a 1.2.

En el suscriptor se cambió la lectura de msg.data por msg.linear.x para obtener y mostrar la velocidad enviada.

## Funcionamiento

El nodo velocity_turtle_pub publica un mensaje Twist cada 0.5 segundos en /turtle1/cmd_vel.

La secuencia enviada es 0.0, 0.1, 0.2 y así sucesivamente hasta 1.2. Medio segundo después de publicar 1.2, envía 0.0 y continúa enviando cero.

El nodo velocity_turtle_subs escucha el mismo tópico. Cada mensaje ejecuta velocity_callback, que obtiene linear.x y muestra su valor con un decimal.

Turtlesim también está suscrito a este tópico y utiliza los mensajes para mover la tortuga. Por eso hay un publicador y dos suscriptores cuando están activos únicamente estos tres programas.

## Configuración del paquete local

Para compilar y ejecutar se utilizó el paquete basics dentro de ~/robotics_ws/src/basics.

Los scripts se colocaron en src/basics/basics y se agregaron estas entradas en la sección console_scripts de setup.py:

```python
'velocity_turtle_pub = basics.velocity_turtle_pub:main',
'velocity_turtle_subs = basics.velocity_turtle_subs:main',
```

En package.xml se agregó la dependencia del mensaje utilizado:

```xml
<depend>geometry_msgs</depend>
```

El repositorio de entrega conserva los cinco archivos solicitados directamente en src. El paquete basics utilizado para colcon está en el entorno local y no está incluido en esta versión del repositorio.

Por ello, los comandos de colcon y ros2 run que se muestran a continuación requieren tener preparado ese paquete local. Los archivos entregados también pueden ejecutarse directamente con python3 después de cargar ROS 2.

## Compilación

Desde la carpeta del workspace:

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select basics
```

## Ejecución

Se inicia primero el simulador, después el suscriptor y al final el publicador para observar la secuencia completa.

### Terminal 1: simulador

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

### Terminal 2: suscriptor

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run basics velocity_turtle_subs
```

### Terminal 3: publicador

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run basics velocity_turtle_pub
```

Los tres programas permanecen activos simultáneamente.

### Ejecución directa de los archivos entregados

Con turtlesim abierto, también se pueden ejecutar los scripts en dos terminales diferentes desde la raíz del repositorio.

Suscriptor:

```bash
source /opt/ros/jazzy/setup.bash
python3 src/velocity_turtle_subs.py
```

Publicador:

```bash
source /opt/ros/jazzy/setup.bash
python3 src/velocity_turtle_pub.py
```

## Comprobación

En una cuarta terminal se carga ROS 2:

```bash
source /opt/ros/jazzy/setup.bash
```

Se revisan los nodos activos y sus conexiones:

```bash
ros2 node list
ros2 node info /velocity_turtle_pub
ros2 node info /velocity_turtle_subs
```

Se revisa el tópico y el contenido de los mensajes:

```bash
ros2 topic info /turtle1/cmd_vel
ros2 topic echo /turtle1/cmd_vel
```

El comando echo se detiene con Ctrl+C. Mientras está activo agrega otra suscripción al tópico.

Se abre el grafo con:

```bash
ros2 run rqt_graph rqt_graph
```

El grafo muestra al publicador conectado a /turtle1/cmd_vel y al tópico conectado con turtlesim y velocity_turtle_subs.

Durante la prueba se observó el recorrido recto de la tortuga y los mensajes de velocidad en las terminales. Al finalizar el incremento, ambos nodos mostraron 0.0 y la tortuga permaneció detenida.

## Problemas y soluciones

Al subir el primer commit de esta actividad, Git rechazó el push porque había cambios en GitHub que no estaban en la copia local.

Se integraron esos cambios con:

```bash
git pull --rebase origin main
```

Después se repitió git push origin main y la subida terminó correctamente.

Para mantener la estructura solicitada en GitHub y poder usar colcon localmente, se conservaron los archivos del paquete basics en la computadora y se prepararon para los commits únicamente los scripts solicitados.

## Evidencia en video de la actividad 2

[Ver video del control de la tortuga](https://drive.google.com/file/d/1M73oRtSIhc--LPFykLb1yMAco8UZOEuU/view?usp=sharing)

## Estructura de entrega después de la actividad 2

```text
Robotics_ws/
└── src/
    ├── README.md
    ├── velocity_publisher.py
    ├── velocity_subscriber.py
    ├── velocity_turtle_pub.py
    └── velocity_turtle_subs.py
```
