import time
from gpiod.line import Direction, Value
import gpiod

GPIO_CHIP = "/dev/gpiochip4"  # Check with `gpioinfo` if unsure
TX_GPIO = 17  # Change this to your actual GPIO pin

# Request GPIO line
with gpiod.request_lines(
    GPIO_CHIP,
    consumer="rf_tx",
    config={
        TX_GPIO: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.INACTIVE
        )
    },
) as request:
    try:
        while True:
            request.set_value(TX_GPIO, Value.ACTIVE)  # Send HIGH signal
            time.sleep(0.5)
            request.set_value(TX_GPIO, Value.INACTIVE)  # Send LOW signal
            time.sleep(2)
            print("Sent RF signal")
    except KeyboardInterrupt:
        print("Exiting...")
