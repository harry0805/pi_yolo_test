import time
import gpiod
from gpiod.line import Direction, Value

# Define GPIO chip and line number (adjust if needed)
GPIO_CHIP = "/dev/gpiochip4"  # Adjust based on your setup
LINE = 17  # GPIO10 (adjust based on your wiring)

# Configure the GPIO line
with gpiod.request_lines(
    GPIO_CHIP,
    consumer="rf-transmitter",
    config={LINE: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)},
) as request:

    def send_signal():
        """Send RF signal by toggling GPIO"""
        bit_sequence = "1111100010"  # Equivalent to Arduino's switchOn("11111", "00010")
        pulse_length = 320  # Adjust if needed

        for _ in range(15):  # Equivalent to setRepeatTransmit(15)
            for bit in bit_sequence:
                request.set_value(LINE, Value.ACTIVE if bit == "1" else Value.INACTIVE)
                time.sleep(pulse_length / 1_000_000)  # Convert microseconds to seconds
            time.sleep(10 * pulse_length / 1_000_000)  # Sync gap

    try:
        while True:
            print("Sending ACTIVE signal...")
            request.set_value(LINE, Value.ACTIVE)  # Switch On
            time.sleep(5)
            print("Sending INACTIVE signal...")
            request.set_value(LINE, Value.INACTIVE)  # Switch Off
            time.sleep(5)
    except KeyboardInterrupt:
        print("Transmission stopped")
    finally:
        request.set_value(LINE, Value.INACTIVE)