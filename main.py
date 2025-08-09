from machine import Pin
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import time

ble = bluetooth.BLE()
sp = BLESimplePeripheral(ble)

led = Pin("LED", Pin.OUT)

# Mode: 0x00 = OFF, 0x01 = ON, 0x02 = BLINK_SLOW, 0x03 = BLINK_FAST
current_mode = 0x00
last_blink_time = time.ticks_ms()
blink_state = False

def on_rx(data: bytes):
    global current_mode
    if data:
        mode = data[0]
        if mode in (0x00, 0x01, 0x02, 0x03):
            current_mode = mode
            print(f"Mode set to {mode}")
        else:
            print(f"Unknown command: {mode}")

sp.on_write(on_rx)

while True:
    now = time.ticks_ms()

    if current_mode == 0x00:
        led.value(0)

    elif current_mode == 0x01:
        led.value(1)

    elif current_mode in (0x02, 0x03):
        interval = 500 if current_mode == 0x02 else 100
        if time.ticks_diff(now, last_blink_time) >= interval:
            blink_state = not blink_state
            led.value(blink_state)
            last_blink_time = now

    time.sleep_ms(10)

