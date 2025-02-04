import gpiod
import time

CHIP = "/dev/gpiochip4"  # Use gpioinfo command to verify the correct chip
TX_GPIO = 17  # Your transmitter GPIO pin

chip = gpiod.Chip(CHIP)
line = chip.get_line(TX_GPIO)

config = gpiod.LineRequest()
config.consumer = "rf_tx"
config.request_type = gpiod.LINE_REQ_DIR_OUT

line.request(config)

try:
    while True:
        line.set_value(1)  # Send HIGH signal
        time.sleep(0.5)
        line.set_value(0)  # Send LOW signal
        time.sleep(2)
except KeyboardInterrupt:
    line.release()
