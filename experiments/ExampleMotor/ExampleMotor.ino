#define motPWM 4
#define motA 16
#define motB 17

void setup() {
  Serial.begin(115200);
  
  pinMode(motPWM, OUTPUT);
  pinMode(motA, OUTPUT);
  pinMode(motB, OUTPUT);
}

void loop() {
  if(Serial.available() > 0){
    float thr = Serial.parseFloat();
    if(thr == 0){
      digitalWrite(motA, LOW);
      digitalWrite(motB, LOW);
    }
    else if(thr > 0){
      digitalWrite(motA, HIGH);
      digitalWrite(motB, LOW);
      analogWrite(motPWM, int(thr * 255));
    }
    else{
      digitalWrite(motA, LOW);
      digitalWrite(motB, HIGH);
      analogWrite(motPWM, int(-thr * 255));
    }
  }

}
