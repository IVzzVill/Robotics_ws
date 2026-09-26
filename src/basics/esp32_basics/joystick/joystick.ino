// Define las entradas analógicas de los dos ejes
#define JOYSTICK_X 34
#define JOYSTICK_Y 35

void setup() {
  // Inicia la comunicación serial con la computadora
  Serial.begin(115200);

  // Configura las lecturas a 12 bits con valores de 0 a 4095
  analogReadResolution(12);
}

void loop() {
  // Obtiene la lectura de cada eje
  int valorX = analogRead(JOYSTICK_X);
  int valorY = analogRead(JOYSTICK_Y);

  // Envía X e Y separados por una coma y termina la línea
  Serial.print(valorX);
  Serial.print(",");
  Serial.println(valorY);

  // Espera 50 milisegundos antes de repetir la lectura
  delay(50);
}
