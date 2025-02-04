from rpi_rf import RFDevice
import time

rfdevice = RFDevice(17)  # GPIO Pin connected to Data pin
rfdevice.enable_tx()

try:
    while True:
        rfdevice.tx_code(1234)  # Send signal
        print("Signal sent!")
        time.sleep(2)
except KeyboardInterrupt:
    rfdevice.cleanup()
