#include <Wire.h>
#include <Adafruit_BMP085.h>

Adafruit_BMP085 bmp;  // Cria um objeto BMP085

void setup() {
  Serial.begin(9600);
  
  if (!bmp.begin()) {
    Serial.println("Não foi possível inicializar o sensor BMP180. Verifique as conexões!");
    while (1);
  }
}

void loop() {
  Serial.print("P{");
  Serial.print(bmp.readPressure());
  Serial.print("};");

  Serial.print("T{");
  Serial.print(bmp.readTemperature());
  Serial.print("};");

  Serial.print("w{");
  Serial.print(20);
  Serial.print("};");

  Serial.print("L{");
  Serial.print(50);
  Serial.println("};");

  delay(1000);  // Aguarda 1 segundo entre leituras
}

