import time
from rpi_rf import RFDevice

GPIO_PIN = 10  # Adjust based on your wiring

rfdevice = RFDevice(GPIO_PIN)
rfdevice.enable_tx()

try:
    while True:
        rfdevice.tx_code(123456, protocol=1, pulse_length=320)  # Adjust code and protocol
        print("Sent ON signal")
        time.sleep(1)
        rfdevice.tx_code(123456, protocol=1, pulse_length=320)  # Adjust for OFF if needed
        print("Sent OFF signal")
        time.sleep(1)
except KeyboardInterrupt:
    print("Transmission stopped")
finally:
    rfdevice.cleanup()
