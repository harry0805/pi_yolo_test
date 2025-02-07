from rpi_rf import RFDevice
import threading
import time

def send_on_signal(rfdevice, stop_event):
    """Continuously sends the ON signal until stop_event is set."""
    global current_mode
    global is_sending
    t_last = time.time_ns()
    while not stop_event.is_set():
        t_now = time.time_ns()
        if current_mode and t_now - t_last >= 1e9:  # 1 second
            is_sending = True
            rfdevice.tx_code(1234)  # Signal for ON
            time.sleep(0.01)  # adjust the interval as needed
            is_sending = False
            t_last = t_now
        else:
            time.sleep(0.01)

PIN = 17  # GPIO pin connected to WL102 DAT

rfdevice = RFDevice(PIN)
rfdevice.enable_tx()

current_mode = False
is_sending = False

stop_event = threading.Event()
on_thread = threading.Thread(target=send_on_signal, args=(rfdevice, stop_event))
on_thread.start()

try:
    while True:
        # Send OFF signal on user input
        print(">>> Sending OFF signal <<<")
        current_mode = False
        if is_sending:
            print("Please slow down!")
            while is_sending:
                time.sleep(0.01)
        rfdevice.tx_code(5678)  # Signal for OFF
        input()

        # Start continuously sending ON signal in a separate thread
        print(">>> Sending ON signal <<<")
        current_mode = True
        input()

except KeyboardInterrupt:
    print("Stopping...")
finally:
    rfdevice.cleanup()