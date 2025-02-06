import pigpio
import time

TX_PIN = 17  # adjust as needed; using BCM numbering
BIT_DURATION = 0.0005  # 500 microseconds per bit, adjust if needed

pi = pigpio.pi()  # Ensure pigpiod is running
if not pi.connected:
    exit(1)

def send_bit(bit):
    if bit:
        pi.write(TX_PIN, 1)
    else:
        pi.write(TX_PIN, 0)
    time.sleep(BIT_DURATION)

def send_byte(byte):
    # Send 8 bits, LSB first
    for i in range(8):
        send_bit((byte >> i) & 1)

def send_message(msg):
    for ch in msg:
        send_byte(ord(ch))

# Setup TX pin
pi.set_mode(TX_PIN, pigpio.OUTPUT)

while True:
    send_message("Hello World!")
    time.sleep(1)
