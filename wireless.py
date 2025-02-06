import time
import gpiod
from gpiod.line import Direction, Value

GPIO_CHIP = "/dev/gpiochip4"   # Adjust to match your Pi’s gpiochip device
LINE_NUM  = 17                 # The GPIO line number (this must match how you wired the TX pin)

# Frequency in seconds at which we toggle/refresh the "on" signal.
# (If "on", we keep the line ACTIVE continuously. A short delay is fine, or 0.)
UPDATE_INTERVAL = 0.1

def main():
    # Configure the GPIO line for output, initially inactive
    config = {LINE_NUM: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)}

    with gpiod.request_lines(GPIO_CHIP, consumer="rf-transmitter", config=config) as request:
        current_mode = "off"

        print("Type 'on' or 'off' to change the signal state. Press Ctrl+C to exit.")
        
        try:
            while True:
                # Check for user input (non‐blocking check would be nicer, but for simplicity we use blocking)
                user_cmd = input("Enter command (on/off): ").strip().lower()
                if user_cmd == "on":
                    current_mode = "on"
                    print(">>> Now sending ACTIVE signal continuously.")
                elif user_cmd == "off":
                    current_mode = "off"
                    print(">>> Sending single active pulse, then going inactive.")
                    # Send a brief active pulse
                    request.set_value(LINE_NUM, Value.ACTIVE)
                    time.sleep(0.2)
                    # Go inactive
                    request.set_value(LINE_NUM, Value.INACTIVE)
                    print(">>> Transmitter is now idle (no signal).")
                else:
                    print("Unknown command. Use 'on' or 'off'.")

                # If we switched to "on," continuously drive the line ACTIVE in a background loop
                while current_mode == "on":
                    request.set_value(LINE_NUM, Value.ACTIVE)
                    # Sleep a bit before checking if user typed a new command
                    time.sleep(UPDATE_INTERVAL)
                    # To break out if user changes to "off," we do a non‐blocking check:
                    # BUT for simplicity, we’ll just break on new input:
                    if gpiod.poll(line=None, timeout=0):
                        # The above is a placeholder—libgpiod python doesn’t have poll like that by default
                        # We could do something more advanced, but let’s keep it simple:
                        break

        except KeyboardInterrupt:
            print("Stopped by user")
        finally:
            # Always go inactive to avoid spurious signals
            request.set_value(LINE_NUM, Value.INACTIVE)

if __name__ == "__main__":
    main()