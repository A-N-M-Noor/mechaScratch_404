#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

TaskHandle_t job;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ }
  
  Serial.println(F("Calculating offsets"));
  // mpu.upsideDownMounting = true;
  mpu.calcOffsets();
  Serial.println("Done!\n");

  xTaskCreatePinnedToCore(loopB,   "secondJob", 1000,   NULL,      1,       &job,            0);
  //                     (function, task name,  memory, parameter, priority, task reference, core)


}

void loop() {
  mpu.update();
}

void loopB(void * param){
  while(true){
    Serial.print("X : ");
    Serial.print(mpu.getAngleX());
    Serial.print("\tY : ");
    Serial.print(mpu.getAngleY());
    Serial.print("\tZ : ");
    Serial.println(mpu.getAngleZ());
    delay(100);
  }
}
