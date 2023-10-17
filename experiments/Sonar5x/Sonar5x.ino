#define MAX_DISTANCE 120

int sPins[] = {26, 27, 32, 33, 25};
int dists[] = {0, 0, 0, 0, 0};

void setup() {
  Serial.begin(115200);
}

void loop() {
  getDistanceValues();

  Serial.print("Sonar Deducted Values: ");
  for(int i = 0; i < 5; i++){
    Serial.print(dists[i]);
    Serial.print(" - ");
  }
  Serial.println(" | ");
  
  delay(30);
}

void getDistanceValues() {
  long sonarTimer = millis();
  for (int i = 0; i < 5; i++) {
    dists[i] = getDistS(sPins[i]);
  }

  while (millis() - sonarTimer < 15) { } // ensures a 15ms delay between pings per sonar
}

int getDistS(int te) {
  pinMode(te, OUTPUT);

  digitalWrite(te, LOW);
  delayMicroseconds(2);
  digitalWrite(te, HIGH);
  delayMicroseconds(10);
  digitalWrite(te, LOW);

  pinMode(te, INPUT);

  long dur = pulseIn(te, HIGH, 7200);
  int dst = dur / 58.8;
  if (dst == 0) dst = MAX_DISTANCE;
  return (dst);
}
