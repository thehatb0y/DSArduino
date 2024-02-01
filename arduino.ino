#include <Wire.h>
#include <Adafruit_BMP085.h>
#include <Servo.h>

Adafruit_BMP085 bmp;  // Cria um objeto BMP085
Servo meuServo;  // Cria um objeto Servo

int pinoLDR = A0;  // Pino analógico ao qual o LDR está conectado
int pinoTransistor1 = 10;  // Pino digital para o primeiro transistor
int pinoTransistor2 = 11;  // Pino digital para o segundo transistor
int pinoServo = 9;  // Pino digital para o micro servo
int valorSerial = 0;

void setup() {
  Serial.begin(9600);  // Inicia a comunicação serial
  pinMode(pinoTransistor1, OUTPUT);  // Configura o pino do primeiro transistor como saída
  pinMode(pinoTransistor2, OUTPUT);  // Configura o pino do segundo transistor como saída
  meuServo.attach(pinoServo);  // Anexa o micro servo ao pino 9
  meuServo.write(90);
  if (!bmp.begin()) {
    Serial.println("Não foi possível inicializar o sensor BMP180. Verifique as conexões!");
    while (1);
  }
}

void loop() {
  // Movimento do servo valores entre 180 e -180
  if (Serial.available() > 0 ) {
    valorSerial = Serial.parseInt();
  if (valorSerial <= 180 && valorSerial >= -180) {
    meuServo.write(meuServo.read() + valorSerial);
  }
  // Transistor 1, 555 on, 554 off
  if (valorSerial == 555 || valorSerial == 554) {
    if (valorSerial == 555){
      digitalWrite(pinoTransistor1, LOW);
    }else{
      digitalWrite(pinoTransistor1, HIGH);
    }
  }

  // Transistor 2, 445 on , 444 off
  if (valorSerial == 445 || valorSerial == 444) {
    if (valorSerial == 445){
      digitalWrite(pinoTransistor2, LOW);
    }else{
      digitalWrite(pinoTransistor2, HIGH);
    }
  }

  }

  // Lê os valores do sensor GY-68
  float temperatura = bmp.readTemperature();
  float pressao = bmp.readPressure();
  
  // Lê o valor do LDR
  int valorLDR = analogRead(pinoLDR);
  

  // Imprime os resultados em uma única linha serial separados por vírgula
  Serial.print("P{");
  Serial.print(pressao);
  Serial.print("},T{");
  Serial.print(temperatura);
  Serial.print("},LDR{");
  Serial.print(valorLDR);
  Serial.print("},T1{");
  Serial.print(digitalRead(pinoTransistor1) == HIGH ? "HIGH" : "LOW");
  Serial.print("},T2{");
  Serial.print(digitalRead(pinoTransistor2) == HIGH ? "HIGH" : "LOW");
  Serial.print("},SP{");
  Serial.print(meuServo.read());  // Imprime a posição atual do servo
  Serial.println("};");


  delay(1000);  // Aguarda 1 segundo entre as leituras
}
