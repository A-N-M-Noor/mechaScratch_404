#include <ESP32Servo.h>

Servo s;

void setup(){
  Serial.begin(115200);
  s.attach(23);
}

void loop(){
  if(Serial.available() > 0){
    int v = Serial.parseInt();
    Serial.println(v);
    if(v>0) s.write(v);
  }
}
