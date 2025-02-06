import time
from rpi_rf import RFDevice

PIN = 17  # GPIO pin connected to WL102 DAT

rfdevice = RFDevice(PIN)
rfdevice.enable_tx()

try:
    while True:
        rfdevice.tx_code(1234)  # Transmit signal
        print("Sent: ON")
        time.sleep(1)
        
        rfdevice.tx_code(5678)  # Transmit another signal for OFF
        print("Sent: OFF")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")
finally:
    rfdevice.cleanup()