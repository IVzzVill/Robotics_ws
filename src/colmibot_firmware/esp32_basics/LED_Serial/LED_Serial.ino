// Define el pin utilizado para el LED
#define LED 2

void setup() {
  // Configura el pin del LED como salida
  pinMode(LED, OUTPUT);

  // Inicia la comunicación serial a 115200 baudios
  Serial.begin(115200);
}

void loop() {
  // Comprueba si llegó un dato por el puerto serial
  if (Serial.available() > 0) {
    // Lee un carácter recibido
    char dato = Serial.read();

    // Enciende el LED cuando recibe el carácter 1
    if (dato == '1') {
      digitalWrite(LED, HIGH);
    }

    // Apaga el LED cuando recibe el carácter 0
    if (dato == '0') {
      digitalWrite(LED, LOW);
    }
  }
}
