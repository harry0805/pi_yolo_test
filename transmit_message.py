from rpi_rf import RFDevice
import threading
import time

def send_on_signal(rfdevice, stop_event):
    """Continuously sends the ON signal until stop_event is set."""
    while not stop_event.is_set():
        rfdevice.tx_code(1234)  # Signal for ON
        print("Sent: ON")
        time.sleep(0.5)  # adjust the interval as needed

PIN = 17  # GPIO pin connected to WL102 DAT

rfdevice = RFDevice(PIN)
rfdevice.enable_tx()

try:
    while True:
        # Send OFF signal on user input
        rfdevice.tx_code(5678)  # Signal for OFF
        print("Sent: OFF")
        input("Press Enter to proceed...")

        # Start continuously sending ON signal in a separate thread
        stop_event = threading.Event()
        on_thread = threading.Thread(target=send_on_signal, args=(rfdevice, stop_event))
        on_thread.start()
        print("Started ON signal thread. Press Enter to stop the continuous ON signal.")
        input()
        stop_event.set()
        on_thread.join()
        print("Stopped ON signal thread.")

except KeyboardInterrupt:
    print("Stopping...")
finally:
    rfdevice.cleanup()