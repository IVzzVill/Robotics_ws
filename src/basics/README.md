# Paquete basics: descripción general

Alumno: Ivan Vazquez Villar

El paquete basics reúne los ejemplos de comunicación entre nodos de ROS 2, control de Turtlesim y comunicación serial con una ESP32 desarrollados durante las actividades.

## Organización actual

- basics/: contiene los nodos Python de velocidad, LED, potenciómetro y joystick
- esp32_basics/: contiene los programas de Arduino y los ejemplos de comunicación serial directa
- launch/: contiene los archivos para iniciar varios nodos con un solo comando
- package.xml: declara las dependencias del paquete
- setup.py: registra los ejecutables y los archivos que se instalan
- setup.cfg y resource/: forman parte de la configuración del paquete
- test/: conserva las pruebas incluidas en el paquete

## Ejemplos incluidos

- velocity_publisher y velocity_subscriber intercambian mensajes Float32 por /velocity
- velocity_turtle_pub y velocity_turtle_subs utilizan Twist para el ejemplo de velocidad de la tortuga
- led_blink y serial_bridge permiten controlar el LED de la ESP32 mediante /led_command
- analog_serial_pub y analog_subs permiten publicar y recibir lecturas del potenciómetro en /analog
- joystick_publisher publica las lecturas de dos ejes en /joystick/raw
- turtle_controller convierte esas lecturas en velocidades para /turtle1/cmd_vel

## Archivos launch

- velocity_system.launch.py inicia el publicador y el suscriptor de velocidad
- turtle_joy_controller.launch.py inicia Turtlesim, el controlador y el publicador del joystick

## Rutas actuales del firmware

- src/basics/esp32_basics/ADC_Pot/ADC_Pot.ino
- src/basics/esp32_basics/LED_Serial/LED_Serial.ino
- src/basics/esp32_basics/joystick/joystick.ino
- src/basics/esp32_basics/serial_led.py
- src/basics/esp32_basics/serial_pot.py

El README se encuentra en src/basics/README.md.

Las secciones anteriores de las actividades se conservan como registro histórico, incluidos sus videos. Sus rutas y árboles reflejan la organización que se utilizó en cada entrega. Para la versión actual se utilizan las rutas indicadas en esta descripción general.

---

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


---

# Actividad 3: Control del LED de la ESP32

## Descripción

En este ejemplo se utiliza ROS 2 para encender y apagar el LED de una ESP32 mediante comunicación serial.

Se comentaron los programas de clase por secciones, conservando su funcionamiento.

## Funcionamiento de los programas

### led_blink.py

Crea el nodo led_blink y publica mensajes std_msgs/msg/Int32 en el tópico /led_command.

El estado comienza en 1 y un temporizador lo alterna entre 1 y 0 cada segundo. Estos valores representan las órdenes de encender y apagar el LED.

### serial_bridge.py

Crea el nodo serial_bridge y se suscribe a /led_command.

Cuando recibe un 1, envía el carácter 1 seguido de un salto de línea por el puerto serial. Cuando recibe un 0, envía el carácter 0.

La conexión utiliza /dev/ttyUSB0 a 115200 baudios.

### LED_Serial.ino

Se ejecuta en la ESP32 y configura el pin 2 como salida.

Lee los caracteres recibidos por serial. Si recibe '1', coloca el pin en HIGH para encender el LED. Si recibe '0', lo coloca en LOW para apagarlo.

### serial_led.py

Permite controlar el LED manualmente desde Python, sin utilizar ROS 2.

Solicita una entrada por teclado: 1 para encender, 0 para apagar y q para salir. Utiliza el mismo puerto y velocidad de comunicación.

Este programa no debe ejecutarse al mismo tiempo que serial_bridge porque ambos necesitan acceder al puerto de la ESP32.

## Organización actual

Los programas ROS 2 se encuentran dentro de src/basics/basics y la configuración del paquete está en src/basics.

El firmware y los programas de comunicación serial directa están en src/colmibot_firmware/esp32_basics.

Los scripts de velocidad de las actividades anteriores también se encuentran ahora dentro de src/basics/basics. Sus secciones anteriores conservan los comandos utilizados en esas entregas.

## Preparación

Se carga LED_Serial.ino en la ESP32 desde Arduino IDE y se cierra el monitor serial antes de ejecutar el puente.

Se comprueba el puerto disponible con:

```bash
ls -l /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
```

En esta práctica la placa apareció como /dev/ttyUSB0.

## Compilación

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select basics
```

## Ejecución con ROS 2

### Terminal 1: puente serial

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run basics serial_bridge
```

### Terminal 2: publicador

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run basics led_blink
```

Los dos nodos permanecen ejecutándose simultáneamente.

## Comprobación

En una tercera terminal:

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 node info /led_blink
ros2 node info /serial_bridge
ros2 topic info /led_command
```

Se comprobó que led_blink publica en /led_command y serial_bridge está suscrito al mismo tópico.

El tipo de mensaje es std_msgs/msg/Int32. Sin herramientas adicionales escuchando, hay un publicador y un suscriptor.

Para observar los mensajes:

```bash
ros2 topic echo /led_command
```

Se observaron valores alternados de 1 y 0. Este comando se detiene con Ctrl+C y agrega una suscripción mientras está activo.

Para mostrar el grafo:

```bash
ros2 run rqt_graph rqt_graph
```

La conexión observada fue:

```text
/led_blink → /led_command → /serial_bridge
```

La ESP32 no aparece como nodo ROS 2 porque recibe las órdenes mediante la conexión serial.

## Resultado y observaciones

El paquete compiló correctamente. El publicador alternó los estados, el puente mostró las órdenes enviadas y el LED de la ESP32 se encendió y apagó.

Al abrir rqt_graph apareció un aviso QSocketNotifier, pero la ventana abrió y permitió comprobar las conexiones.

Después se agregaron comentarios a los archivos. Se comparó la estructura del código Python con la versión original para confirmar que se conservó su lógica. En el firmware se revisó que los cambios fueran únicamente comentarios y formato.

## Evidencia del ejemplo del LED

[Ver video del LED controlado con ROS 2](https://drive.google.com/file/d/1F7s_RSn5VcQd6ww2n6IhPIkxh7u9KqnB/view?usp=drive_link)


---

# Ejemplo del potenciómetro con ESP32 y ROS 2

## Descripción

En este ejemplo se lee un potenciómetro con la ESP32 y se envían sus lecturas a ROS 2 mediante comunicación serial.

Se utilizan dos nodos: uno recibe las lecturas de la placa y las publica, mientras el otro recibe los mensajes y muestra los valores en la terminal.

## Funcionamiento de los programas

### ADC_Pot.ino

Se ejecuta en la ESP32 y lee la entrada analógica del GPIO 15 mediante analogRead.

Envía cada lectura por serial a 115200 baudios, seguida de un salto de línea. Después espera 100 milisegundos antes de repetir el proceso.

### analog_serial_pub.py

Crea el nodo analog_serial_pub y abre /dev/ttyUSB0 a 115200 baudios.

Un temporizador revisa el puerto cada 0.01 segundos. Cuando hay datos disponibles, lee una línea y comprueba que contenga dígitos.

Convierte la lectura a entero y la publica en el campo data de un mensaje std_msgs/msg/Int32 en el tópico /analog.

La revisión cada 0.01 segundos no significa que se publiquen 100 lecturas por segundo, porque la publicación depende de los datos enviados por la ESP32.

### analog_subs.py

Crea el nodo analog_subscriber y se suscribe a /analog.

Cuando recibe un mensaje, ejecuta analog_callback, obtiene msg.data y muestra la lectura con la etiqueta ADC.

Los valores mostrados son lecturas del convertidor analógico a digital, no voltajes calculados.

### serial_pot.py

Lee y muestra directamente las líneas enviadas por la ESP32 mediante Python, sin utilizar ROS 2.

Utiliza el mismo puerto serial, por lo que no debe ejecutarse simultáneamente con analog_serial_pub ni con el monitor serial de Arduino.

## Preparación

Se carga el archivo ADC_Pot.ino en la ESP32 desde Arduino IDE.

La señal del potenciómetro se conecta al GPIO 15 y sus extremos a 3.3 V y GND.

Antes de iniciar los nodos se cierra el monitor serial y cualquier programa que esté utilizando el puerto.

## Compilación

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select basics
```

## Ejecución

### Terminal 1: suscriptor

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run basics analog_subs
```

El nombre del ejecutable es analog_subs y el nombre del nodo es analog_subscriber.

### Terminal 2: publicador serial

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run basics analog_serial_pub
```

Los dos nodos permanecen activos mientras se gira el potenciómetro.

## Comprobación

En una tercera terminal:

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 node info /analog_serial_pub
ros2 node info /analog_subscriber
ros2 topic info /analog
```

El tópico /analog utiliza std_msgs/msg/Int32. Con únicamente los dos nodos del ejemplo activos, tiene un publicador y un suscriptor.

Para observar las lecturas:

```bash
ros2 topic echo /analog
```

Los valores del campo data cambian al girar el potenciómetro. Se detiene echo con Ctrl+C antes de continuar.

Para abrir el grafo:

```bash
ros2 run rqt_graph rqt_graph
```

La conexión observada es:

```text
/analog_serial_pub → /analog → /analog_subscriber
```

La ESP32 no aparece como nodo ROS 2 porque se comunica con el publicador mediante el puerto serial.

## Resultado y observaciones

Primero se comprobó en el monitor serial de Arduino que los números cambiaban al girar el potenciómetro.

Después se cerró el monitor y se ejecutaron los nodos. Las lecturas aparecieron en el suscriptor y en ros2 topic echo. El grafo permitió comprobar la conexión entre ambos nodos.

No fue necesario modificar la lógica de los programas durante esta prueba. Se agregaron comentarios por sección y se compararon los archivos con sus versiones originales para comprobar que se conservó el código.

## Evidencia del ejemplo del potenciómetro

[Ver video del potenciómetro con ROS 2](https://drive.google.com/file/d/1L5_tvLl4-Yc6a2bpFejC-KEC-WTcxuf0/view?usp=drive_link)

## Control de versiones de los ejemplos de ESP32

El desarrollo se organizó en cinco commits:

1. Archivos y ejemplos vistos en clase
2. Comprobación y comentarios del ejemplo del LED
3. Documentación y video del LED
4. Comprobación y comentarios del ejemplo del potenciómetro
5. Documentación y video del potenciómetro

## Estructura actual de la entrega

Los archivos de configuración se conservan para permitir la compilación del paquete basics con colcon.

```text
src/
├── README.md
├── basics/
│   ├── basics/
│   │   ├── __init__.py
│   │   ├── velocity_publisher.py
│   │   ├── velocity_subscriber.py
│   │   ├── velocity_turtle_pub.py
│   │   ├── velocity_turtle_subs.py
│   │   ├── led_blink.py
│   │   ├── serial_bridge.py
│   │   ├── analog_serial_pub.py
│   │   └── analog_subs.py
│   ├── package.xml
│   ├── setup.py
│   ├── setup.cfg
│   ├── resource/
│   │   └── basics
│   └── test/
│       ├── test_copyright.py
│       ├── test_flake8.py
│       └── test_pep257.py
└── colmibot_firmware/
    └── esp32_basics/
        ├── ADC_Pot/
        │   └── ADC_Pot.ino
        ├── LED_Serial/
        │   └── LED_Serial.ino
        ├── serial_led.py
        └── serial_pot.py
```

Esta estructura reemplaza las ubicaciones de las entregas anteriores. Sus explicaciones y enlaces de evidencia se conservan como registro de esas actividades.


## Configuración final del control con joystick

Se conservaron los centros medidos: 1835 para el primer eje y 1765 para el segundo.

Se utiliza una zona muerta de ±100 unidades alrededor de cada centro. En la muestra tomada sin tocar el joystick, el primer eje varió aproximadamente entre 1825 y 1840 y el segundo entre 1755 y 1775. El margen elegido cubre esas variaciones y permite mantener la tortuga detenida en posición neutral.

Se conservaron los límites de velocidad lineal de ±1.5 y angular de ±1.5 rad/s, porque durante la prueba permitieron controlar el movimiento de la tortuga de forma manejable.

Fuera de la zona muerta, la velocidad aumenta proporcionalmente hasta el límite de cada eje. Se calcula cada lado por separado porque los centros medidos no coinciden con la mitad del rango de 0 a 4095.

El controlador también envía velocidad cero si deja de recibir lecturas válidas durante más de 0.5 segundos.


---

# Control de Turtlesim con joystick y ESP32

## Descripción

Se integró un joystick de dos ejes con una ESP32 y dos nodos de ROS 2 para controlar el movimiento de una tortuga.

La ESP32 obtiene las lecturas analógicas y las envía por serial. El publicador transmite esas lecturas por un tópico de ROS 2. El controlador recibe los valores y los convierte en velocidades lineal y angular.

## Conexiones

Se utilizó la siguiente asignación de pines:

| Joystick | ESP32 |
|----------|-------|
| VCC | 3V3 |
| GND | GND |
| VRx | GPIO 34 |
| VRy | GPIO 35 |
| SW | Sin conectar |

Se eligieron GPIO 34 y GPIO 35 porque son entradas con ADC1. El joystick se alimentó con 3.3 V para mantener sus señales dentro del nivel de alimentación de la ESP32.

## Archivos generados

### joystick.ino

Ubicación:

```text
src/basics/colmibot_firmware/esp32_basics/joystick/joystick.ino
```

Configura la resolución del ADC a 12 bits y lee ambos ejes, con valores entre 0 y 4095.

Envía los datos a 115200 baudios con el formato X,Y y un salto de línea. Después espera 50 milisegundos antes de repetir.

### joystick_publisher.py

Ubicación:

```text
src/basics/basics/joystick_publisher.py
```

Crea el nodo joystick_publisher y abre /dev/ttyUSB0 a 115200 baudios.

Acumula los bytes recibidos hasta completar una línea. Separa los dos números y descarta líneas inválidas o valores fuera del rango de 12 bits.

Publica las lecturas en /joystick/raw mediante std_msgs/msg/Int32MultiArray:

```text
data: [lectura_GPIO34, lectura_GPIO35]
```

Este nodo no envía órdenes a Turtlesim.

### turtle_controller.py

Ubicación:

```text
src/basics/basics/turtle_controller.py
```

Crea el nodo turtle_controller y se suscribe a /joystick/raw.

Convierte las lecturas en velocidades y publica mensajes geometry_msgs/msg/Twist en /turtle1/cmd_vel.

Utiliza linear.x para avanzar o retroceder y angular.z para girar. Ambas velocidades se calculan de manera independiente, por lo que pueden actuar simultáneamente.

## Orientación y calibración

Con la orientación física utilizada se obtuvieron estas lecturas aproximadas:

| Posición | GPIO 34 | GPIO 35 |
|----------|---------|---------|
| Centro | 1835 | 1765 |
| Adelante | 0 | 1765 |
| Atrás | 4095 | 1765 |
| Izquierda | 1835 | 4095 |
| Derecha | 1835 | 0 |

Se invirtió el signo del primer eje para que mover el joystick hacia adelante produzca velocidad lineal positiva.

El segundo eje produce giro positivo hacia la izquierda y negativo hacia la derecha.

## Zona muerta y control proporcional

Se conservaron los centros 1835 y 1765 y una zona muerta de ±100 unidades.

Esto corresponde a los intervalos:

- Primer eje: de 1735 a 1935
- Segundo eje: de 1665 a 1865

Dentro del intervalo correspondiente, la velocidad de ese eje es cero. El margen de 100 unidades equivale aproximadamente al 2.4 % del rango completo del ADC por cada lado.

En reposo se observaron valores aproximados de 1825 a 1840 en el primer eje y de 1755 a 1775 en el segundo. La zona muerta cubre esas variaciones.

Fuera de la zona muerta, se resta ese margen y se escala el recorrido restante hasta el extremo del ADC. Cada lado se calcula por separado porque el centro real no es 2048.

Así, la velocidad aumenta progresivamente desde cero hasta su límite y no funciona como un control de encendido y apagado.

## Límites y detención

Se conservaron los siguientes límites después de las pruebas:

- Velocidad lineal: de -1.5 a 1.5
- Velocidad angular: de -1.5 a 1.5 rad/s

Estos límites permitieron observar cambios proporcionales y manejar la tortuga durante las pruebas. Es necesario realizar movimientos breves para evitar alcanzar las paredes del simulador.

El controlador publica cada 0.05 segundos. Si pasan más de 0.5 segundos sin recibir una lectura válida, envía velocidades cero.

## Configuración del paquete

Se agregaron estas entradas en console_scripts de src/basics/setup.py, conservando las anteriores:

```python
'joystick_publisher = basics.joystick_publisher:main',
'turtle_controller = basics.turtle_controller:main',
```

Se utilizan rclpy, std_msgs, geometry_msgs y la biblioteca de comunicación serial utilizada en los ejemplos anteriores.

## Compilación y preparación

Se carga joystick.ino en la ESP32 desde Arduino IDE y se cierra el monitor serial antes de ejecutar el publicador.

Desde el workspace:

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select basics
```

No deben ejecutarse otros programas que utilicen el mismo puerto serial ni otros publicadores de velocidad para la tortuga durante esta prueba.

## Ejecución

### Terminal 1: simulador

```bash
source /opt/ros/jazzy/setup.bash
ros2 run turtlesim turtlesim_node
```

### Terminal 2: controlador

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run basics turtle_controller
```

### Terminal 3: publicador serial

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run basics joystick_publisher
```

## Comprobación

En otra terminal:

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 node info /joystick_publisher
ros2 node info /turtle_controller
ros2 topic info /joystick/raw
ros2 topic info /turtle1/cmd_vel
```

Para observar las lecturas del joystick:

```bash
ros2 topic echo /joystick/raw
```

Después de detener ese comando con Ctrl+C, se pueden observar las velocidades:

```bash
ros2 topic echo /turtle1/cmd_vel
```

Para abrir el grafo:

```bash
ros2 run rqt_graph rqt_graph
```

La comunicación esperada es:

```text
/joystick_publisher
        ↓
/joystick/raw
        ↓
/turtle_controller
        ↓
/turtle1/cmd_vel
        ↓
/turtlesim
```

Para reiniciar la escena se suelta primero el joystick y se ejecuta:

```bash
ros2 service call /reset std_srvs/srv/Empty "{}"
```

## Pruebas y problemas encontrados

Se probó el avance, retroceso, giro hacia ambos lados y movimiento combinado. También se comprobó que la velocidad cambia con la inclinación y que la tortuga se detiene al soltar el joystick.

Los centros medidos fueron distintos de 2048. Se utilizaron los valores reales para evitar calcular el movimiento respecto a un centro incorrecto.

Las lecturas variaban ligeramente con el joystick suelto. Se estableció la zona muerta para que esas variaciones no generaran movimiento.

Según la orientación del módulo, el primer eje correspondía a adelante y atrás y el segundo al giro. Se ajustó la conversión a esa orientación sin cambiar los cables.

Durante las pruebas la tortuga alcanzó las paredes y Turtlesim mostró avisos. Se reinició la escena y se realizaron movimientos más breves.

El controlador puede mostrar -0.00 en la velocidad lineal al estar centrado debido a la inversión del signo. Ese valor equivale a cero.

## Control de versiones

Se organizaron seis etapas:

1. Programa de Arduino y comprobación de las lecturas del joystick
2. Verificación del publicador serial
3. Verificación de recepción en el suscriptor
4. Primera versión de envío de velocidades a Turtlesim
5. Confirmación de límites y zona muerta
6. Documentación completa y evidencia

## Evidencia en video

[Ver video del joystick controlando Turtlesim](https://drive.google.com/file/d/1V4_MCRjbAE4Etz-Wf2883Qd3GcCYuM1r/view?usp=sharing)

## Archivos agregados al workspace

Se conservaron los archivos de las actividades anteriores y se agregaron:

```text
src/basics/
├── basics/
│   ├── joystick_publisher.py
│   └── turtle_controller.py
└── colmibot_firmware/
    └── esp32_basics/
        └── joystick/
            └── joystick.ino
```


---

# Ejecución de nodos mediante un archivo launch

## Descripción

En esta actividad se creó velocity_system.launch.py para iniciar los nodos velocity_publisher y velocity_subscriber mediante un solo comando, siguiendo el ejemplo de la presentación de clase.

Los dos nodos se ejecutan como procesos separados y muestran sus mensajes en la misma terminal.

## Funcionamiento y configuración

El archivo se encuentra en:

```text
src/basics/launch/velocity_system.launch.py
```

La función generate_launch_description devuelve una LaunchDescription con dos acciones Node. Cada acción indica el paquete basics, el ejecutable correspondiente y output='screen' para mostrar su salida en la terminal.

El publicador envía mensajes std_msgs/msg/Float32 por /velocity cada 0.5 segundos. El suscriptor recibe los datos y muestra la velocidad.

Se agregó el archivo launch a data_files en setup.py para instalarlo dentro de share/basics/launch. También se declararon launch y launch_ros como dependencias de ejecución en package.xml.

## Compilación y ejecución

```bash
cd ~/robotics_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select basics
source install/setup.bash
ros2 launch basics velocity_system.launch.py
```

No se deben iniciar copias adicionales de los mismos nodos durante esta comprobación.

## Comprobación

Con el launch ejecutándose, en otra terminal:

```bash
source /opt/ros/jazzy/setup.bash
ros2 node list
ros2 node info /velocity_publisher
ros2 node info /velocity_subscriber
ros2 topic info /velocity
ros2 topic echo /velocity
```

Se comprobó la presencia de ambos nodos y del tópico /velocity con mensajes Float32. Antes de iniciar echo, el tópico tenía un publicador y un suscriptor.

Los valores publicados coincidieron con los recibidos. También se observó que la secuencia llegaba a 1.5 y regresaba a 0.0.

Después de detener echo con Ctrl+C, se abrió el grafo:

```bash
ros2 run rqt_graph rqt_graph
```

La conexión observada fue:

```text
/velocity_publisher → /velocity → /velocity_subscriber
```

## Resultado

El launch permitió ejecutar ambos nodos desde una sola terminal y comprobar su comunicación sin modificar los programas originales.

## Evidencia en video

[Ver video de la ejecución con launch](https://drive.google.com/file/d/1kf8mtKcoTKCxSf0hDiybt8Whktv2IIkN/view?usp=sharing)


---

# Integración final mediante turtle_joy_controller.launch.py

## Descripción

Se creó un launch para iniciar los tres nodos del sistema de control con joystick mediante un solo comando.

El launch inicia los procesos y muestra sus salidas en la terminal. La comunicación entre nodos continúa realizándose mediante tópicos.

## Funcionamiento

1. joystick_publisher recibe por serial las lecturas de la ESP32 y las publica en /joystick/raw como std_msgs/msg/Int32MultiArray
2. turtle_controller recibe las lecturas, aplica los centros, la zona muerta y los límites, y publica geometry_msgs/msg/Twist en /turtle1/cmd_vel
3. turtlesim recibe las velocidades y mueve la tortuga

El publicador del joystick no envía órdenes directamente a Turtlesim.

## Configuración

El archivo se encuentra en src/basics/launch/turtle_joy_controller.launch.py.

Se registraron ambos launch dentro de data_files en setup.py. Se agregaron turtlesim y python3-serial como dependencias de ejecución en package.xml, conservando launch y launch_ros.

Se trasladó el README a src/basics y se reunieron los programas de la ESP32 en src/basics/esp32_basics. Se conservaron los nodos, los dos launch y las evidencias anteriores.

## Preparación y compilación

La ESP32 debe tener cargado joystick.ino y estar conectada al puerto configurado, /dev/ttyUSB0.

Se cierra el monitor serial y cualquier programa que esté utilizando el puerto. También se detienen copias anteriores de los nodos del sistema.

Desde la terminal se ejecutan estos comandos en orden:

    cd ~/robotics_ws
    source /opt/ros/jazzy/setup.bash
    colcon build --packages-select basics
    source install/setup.bash

## Ejecución

Se inicia todo el sistema con:

    ros2 launch basics turtle_joy_controller.launch.py

Deben iniciarse turtlesim_node, turtle_controller y joystick_publisher.

Al mover el joystick, la tortuga avanza, retrocede y gira. Al soltarlo, la zona muerta mantiene las velocidades en cero.

## Comprobación

En otra terminal se ejecuta:

    source /opt/ros/jazzy/setup.bash
    ros2 node list
    ros2 node info /turtle_controller
    ros2 topic info /joystick/raw
    ros2 topic info /turtle1/cmd_vel

Los nodos esperados son /joystick_publisher, /turtle_controller y /turtlesim.

Con únicamente esos nodos activos, cada uno de los dos tópicos tiene un publicador y un suscriptor.

Para observar las velocidades se ejecuta:

    ros2 topic echo /turtle1/cmd_vel

Se mueve el joystick para comprobar los cambios de linear.x y angular.z. Después se detiene echo con Ctrl+C y se abre el grafo:

    ros2 run rqt_graph rqt_graph

El grafo muestra esta comunicación:

    /joystick_publisher → /joystick/raw → /turtle_controller
    /turtle_controller → /turtle1/cmd_vel → /turtlesim

## Problema encontrado

En el primer intento el publicador no pudo abrir /dev/ttyUSB0 porque el puerto no estaba disponible. La compilación había terminado correctamente y los otros dos procesos sí iniciaron.

Se revisó la conexión de la ESP32 y la disponibilidad del puerto. Después se volvió a ejecutar el launch y se recibieron las lecturas correctamente.

El puerto se puede comprobar con:

    ls -l /dev/ttyUSB* /dev/ttyACM* 2>/dev/null

## Resultado

Se comprobó que el launch inicia el sistema desde una sola terminal y que la tortuga responde al joystick. También se verificaron los nodos, los tópicos y sus conexiones mediante el grafo de ROS.

## Evidencia en video

[Ver video de la integración con launch](https://drive.google.com/file/d/1uFpuQ0Rokv2Qp6WF__dg9Rt1VSwW-Owc/view?usp=drive_link)

## Control de versiones

- Commit inicial con el launch funcionando
- Commit final con la documentación y la reestructura del paquete basics
