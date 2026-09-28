# used for testing the latency of the keypad
# same as main.py but it times how long send_keys() takes
# every time a key is pressed or released, then prints min/max/avg
# copy this onto the board as main.py, open PuTTY with the COM port
# for the keypad and speed 115200, then press the keys until it prints
# 20 samples = about 10 key presses (a press and a release each count)
# this only measures how long the firmware takes to send the report,
# not the whole delay from pressing to the game seeing it

import usb.device
from usb.device.keyboard import KeyboardInterface, KeyCode
from machine import Pin
import time

SAMPLES = 20

KEYS = (
    (Pin.cpu.GPIO0, KeyCode.Z),
    (Pin.cpu.GPIO1, KeyCode.X)
)

class OSUKeypad(KeyboardInterface):
    pass

def osu_keypad():
    for pin, _ in KEYS:
        pin.init(Pin.IN, Pin.PULL_UP)

    k = OSUKeypad()
    usb.device.get().init(k, builtin_driver=True)

    keys = []
    prev_keys = [None]
    timings = []
    reported = False

    while True:
        if k.is_open():

            while k.busy():
                time.sleep_ms(1)

            keys.clear()
            for pin, code in KEYS:
                if not pin():
                    keys.append(code)

            if keys != prev_keys:
                start = time.ticks_us()
                k.send_keys(keys)
                elapsed = time.ticks_diff(time.ticks_us(), start)

                prev_keys.clear()
                prev_keys.extend(keys)

                if not reported:
                    timings.append(elapsed)
                    if len(timings) >= SAMPLES:
                        print("samples:", len(timings))
                        print("min:", min(timings), "us")
                        print("max:", max(timings), "us")
                        print("avg:", sum(timings) / len(timings), "us")
                        reported = True

        time.sleep_ms(1)

osu_keypad()
