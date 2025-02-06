import time
import gpiod
from gpiod.line import Direction, Value
import threading

GPIO_CHIP = "/dev/gpiochip4"   # Adjust to match your Pi’s gpiochip device
LINE_NUM  = 17                 # The GPIO line number (this must match how you wired the TX pin)

# Frequency in seconds at which we toggle/refresh the "on" signal.
# (If "on", we keep the line ACTIVE continuously. A short delay is fine, or 0.)
UPDATE_INTERVAL = 2

current_mode = {"state": False}  # shared mutable mode
stop_event = threading.Event()

def signal_toggle_loop(request):
    while not stop_event.is_set():
        if current_mode["state"]:
            request.set_value(LINE_NUM, Value.ACTIVE)
            time.sleep(0.1)
            request.set_value(LINE_NUM, Value.INACTIVE)
            time.sleep(UPDATE_INTERVAL)
        else:
            time.sleep(0.1)

def main():
    # Configure the GPIO line for output, initially inactive
    config = {LINE_NUM: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)}

    with gpiod.request_lines(GPIO_CHIP, consumer="rf-transmitter", config=config) as request:
        toggle_thread = threading.Thread(target=signal_toggle_loop, args=(request,), daemon=True)
        toggle_thread.start()
        
        try:
            while True:
                # Check for user input (non‐blocking check would be nicer, but for simplicity we use blocking)
                if current_mode["state"]:
                    print(">>> Now sending ACTIVE signal continuously <<<")
                else:
                    current_mode["state"] = False
                    # Send one last INACTIVE signal before going idle
                    request.set_value(LINE_NUM, Value.INACTIVE)
                    print(">>> Transmitter is now idle (no signal) <<<")
                input("").strip().lower()
                current_mode["state"] = not current_mode["state"]

        except KeyboardInterrupt:
            print("Stopped by user")
        finally:
            current_mode["state"] = False
            request.set_value(LINE_NUM, Value.INACTIVE)
            stop_event.set()
            toggle_thread.join()

if __name__ == "__main__":
    main()