const int dataPin = 2;       // Hooked to Receiver Data Out
const int relayPin = 7;      // Controls the light (via a relay module)

// Batch parameters & detection threshold
const float activeThreshold = 0.99;  // Active state if LOW percentage exceeds this
const unsigned long batchDuration = 10;  // Batch duration in ms

const unsigned long inactiveTimeout = 5000;  // Turns relay off if no active signal for this long (ms)

// Data structure to record timing for consecutive states
struct StateTiming {
  bool active;             // true if state was active, false otherwise
  unsigned long duration;  // Duration in milliseconds
};

const int maxTimings = 50;   // Maximum number of state recordings
StateTiming stateTimings[maxTimings];
int timingCount = 0;

// Tracking current state timing
bool currentState = false;         // Initial state, assume inactive
unsigned long stateStartTime = 0;  // Timestamp when current state started
unsigned long lastActiveTime = 0;  // New global variable to track last time an active batch was detected

void setup() {
  Serial.begin(9600);
  pinMode(dataPin, INPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // Relay off HIGH=off
  
  // Initialize current state start time
  stateStartTime = millis();
  
  Serial.println("System initialized, light OFF.");
}

void loop() {
  // Collect samples over a fixed time window (batchDuration)
  unsigned long batchStart = millis();
  int totalSamples = 0;
  int countLow = 0;
  while ((millis() - batchStart) < batchDuration) {
    totalSamples++;
    if (digitalRead(dataPin) == LOW) {
      countLow++;
    }
  }
  float lowRatio = (float) countLow / totalSamples;
  // Determine current batch state using the threshold
  bool batchState = (lowRatio > activeThreshold);
  
  // If state changes, record the ending duration of the previous state
  if (batchState != currentState) {
    unsigned long now = millis();
    unsigned long duration = now - stateStartTime;
    if (timingCount < maxTimings) {
      stateTimings[timingCount++] = { currentState, duration };
    }
    // Debug print: record state change
    Serial.print(batchState ? "ACTIVE" : "INACTIVE");
    Serial.print(" after ");
    Serial.print(duration);
    Serial.println(" ms");
    
    currentState = batchState;
    stateStartTime = now;
  }
  
  // // Updated relay control:
  // unsigned long now = millis();
  // if (batchState) {
  //   lastActiveTime = now;
  //   if (digitalRead(relayPin) == HIGH) {
  //     Serial.println("Carrier detected -> Light ON");
  //     digitalWrite(relayPin, LOW);
  //   }
  // } else if ((now - lastActiveTime) > inactiveTimeout) {
  //   if (digitalRead(relayPin) == LOW) {
  //     Serial.println("No active signal for a while -> Light OFF");
  //     digitalWrite(relayPin, HIGH);
  //   }
  // }
}