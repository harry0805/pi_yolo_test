import gpiod
import time

TX_PIN = 17  # adjust as needed
BIT_DURATION = 0.0005  # 500 microseconds per bit

# Initialize gpiod chip and request TX line as output
chip = gpiod.Chip('/dev/gpiochip0')
line = chip.get_line(TX_PIN)
line.request(consumer="transmit_message", type=gpiod.LINE_REQ_DIR_OUT)

def send_bit(bit):
    line.set_value(1 if bit else 0)
    time.sleep(BIT_DURATION)

def send_byte(byte):
    # Send 8 bits, LSB first
    for i in range(8):
        send_bit((byte >> i) & 1)

def send_message(msg):
    for ch in msg:
        send_byte(ord(ch))

while True:
    send_message("Hello World!")
    time.sleep(1)
