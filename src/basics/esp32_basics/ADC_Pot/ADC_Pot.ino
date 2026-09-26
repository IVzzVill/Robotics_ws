// Define el pin conectado a la señal del potenciómetro
#define POT 15

void setup() {
  // Inicia la comunicación serial a 115200 baudios
  Serial.begin(115200);
}

void loop() {
  // Obtiene la lectura analógica del potenciómetro
  int valor = analogRead(POT);

  // Envía la lectura por serial seguida de un salto de línea
  Serial.println(valor);

  // Espera 100 milisegundos antes de repetir la lectura
  delay(100);
}
