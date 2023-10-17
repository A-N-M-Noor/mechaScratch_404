#include <ESP32Servo.h>

Servo s;
#define servoPin 18
int steerAngle = 25;

void setup() {
  Serial.begin(115200);
  s.attach(servoPin);
  s.write(90);
}

void loop() {
  for(int p = 90; p < 90 + steerAngle; p++){
    s.write(p);
    Serial.print("Steer angle: ");
    Serial.println(p - 90);
    delay(5);
  }

  for(int p = 90 + steerAngle; p >= 0; p--){
    s.write(p);
    Serial.print("Steer angle: ");
    Serial.println(p - 90);
    delay(5);
  }

  for(int p = 0; p < 90; p++){
    s.write(p);
    Serial.print("Steer angle: ");
    Serial.println(p - 90);
    delay(5);
  }

}
