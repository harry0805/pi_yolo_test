#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();

const int dataPin = 2;  // Hooked to Receiver Data Out
const int relayPin = 7; // Controls the light (via a relay module)

const unsigned long RELAY_TIMEOUT = 5000; // Timeout in milliseconds

unsigned long lastActiveTime = 0;

void setup()
{
  Serial.begin(9600);

  mySwitch.enableReceive(digitalPinToInterrupt(dataPin));

  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // Relay off HIGH=off

  Serial.println("System initialized!");
}

void loop()
{
  unsigned long now = millis();

  if (mySwitch.available())
  {
    unsigned long receivedValue = mySwitch.getReceivedValue();
    Serial.print("Received ");
    Serial.println(receivedValue);

    if (receivedValue == 1234)
    {
      Serial.println("Light ON");
      digitalWrite(relayPin, LOW);
      lastActiveTime = now;
    }
    else if (receivedValue == 5678)
    {
      Serial.println("Light OFF");
      digitalWrite(relayPin, HIGH);
    }

    mySwitch.resetAvailable();
  }

  // Turn off relay if no "ON" signal received for the timeout duration
  if (digitalRead(relayPin) == LOW && (now - lastActiveTime > RELAY_TIMEOUT))
  {
    Serial.println("Timeout reached -> Light OFF");
    digitalWrite(relayPin, HIGH);
  }
}