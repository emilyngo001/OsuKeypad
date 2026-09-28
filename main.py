import usb.device
from usb.device.keyboard import KeyboardInterface, KeyCode
from machine import Pin
import time

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
        
    while True:
        if k.is_open():
        
            while k.busy():
                time.sleep_ms(1)
                
            keys.clear()
            for pin, code in KEYS:
                if not pin():
                    keys.append(code)
            
            if keys != prev_keys:
                k.send_keys(keys)
                prev_keys.clear()
                prev_keys.extend(keys)
                
        time.sleep_ms(1)
        
osu_keypad()
                

