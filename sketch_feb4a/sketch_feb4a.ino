const int dataPin = 2;
const int detectionTimeframe = 100;
bool currentState = false;

const int relayPin = 7;

void setup() {
  Serial.begin(9600);
  pinMode(dataPin, INPUT);

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // Ensure relay is OFF initially
}

void loop() {
  unsigned long start = millis();
  int countLow  = 0;
  int countHigh = 0;

  // Sample the data pin for 50 milliseconds:
  while (millis() - start < detectionTimeframe) {
    int val = digitalRead(dataPin);
    if (val == LOW) {
      countLow++;
    } else {
      countHigh++;
    }
  }

  // Serial.print(countLow);
  // Serial.print("-");
  // Serial.println(countHigh);
  float lowPercentage = (float)countLow / (countLow + countHigh);
  Serial.println(lowPercentage);
  // Decide if the signal was mostly LOW(ACTIVE SIGNAL)
  if (lowPercentage > 0.95) {
    if (!currentState){
      Serial.println("ACTIVE");
      digitalWrite(relayPin, LOW);
    }
    currentState = true;
  } else {
    if (currentState){
      Serial.println("INACTIVE");
      digitalWrite(relayPin, HIGH);
    }
    currentState = false;
  }
}