import time
import gpiod
from gpiod.line import Direction, Value  # import necessary enums

TX_PIN = 17  # adjust as needed
BIT_DURATION = 0.0005  # 500 microseconds per bit

def send_bit(request, bit):
    request.set_value(TX_PIN, Value.ACTIVE if bit else Value.INACTIVE)
    time.sleep(BIT_DURATION)

def send_byte(request, byte):
    # Send 8 bits, LSB first
    for i in range(8):
        send_bit(request, (byte >> i) & 1)

def send_message(request, msg):
    for ch in msg:
        send_byte(request, ord(ch))

with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="transmit_message",
    config={TX_PIN: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)}
) as req:
    while True:
        send_message(req, "Hello World!")
        time.sleep(1)
