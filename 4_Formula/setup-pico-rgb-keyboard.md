# Formula: Setup Pico 2 W RGB Keyboard (Stream Deck Style)

## Overview

This sets up a Raspberry Pi Pico 2 W with a **Pimoroni RGB Keypad Base** (4×4 = 16 keys with APA102 RGB LEDs) as a Stream Deck-style macro keyboard, usable with OBS, streaming, or custom shortcuts.

---

## Hardware Required

- Raspberry Pi Pico 2 W
- [Pimoroni Pico RGB Keypad Base](https://shop.pimoroni.com/en-us/products/pico-rgb-keypad-base) (4×4 RGB silicone keypad)
- USB cable (data-capable)

---

## Step 1 — Flash MicroPython with Pimoroni Libraries

Pimoroni provides a custom MicroPython UF2 that includes all RGB keypad drivers.

1. Enter BOOTSEL mode:
   - Hold **BOOTSEL**, plug in USB, release after 3 seconds
   - `RPI-RP2` volume should appear

2. Download Pimoroni MicroPython for Pico 2 W:
   - https://github.com/pimoroni/pimoroni-pico/releases
   - Look for: `pimoroni-pico2w-*.uf2`

3. Drag the `.uf2` onto the `RPI-RP2` volume — Pico reboots automatically

---

## Step 2 — Connect via Serial

```bash
# Find port
ls /dev/cu.usb*

# Open REPL
screen /dev/cu.usbmodem* 115200
```

Verify Pimoroni firmware loaded:
```python
import picokeypad
print("Keypad ready")
```

---

## Step 3 — Basic RGB Keypad Script

Save this as `main.py` on the Pico:

```python
import picokeypad as keypad
import time

keypad.init()
keypad.set_brightness(1.0)

NUM_PADS = keypad.get_num_pads()

# Define key colors (R, G, B) per key index 0-15
COLORS = [
    (255, 0, 0),    # 0 - Red
    (0, 255, 0),    # 1 - Green
    (0, 0, 255),    # 2 - Blue
    (255, 255, 0),  # 3 - Yellow
    (255, 0, 255),  # 4 - Magenta
    (0, 255, 255),  # 5 - Cyan
    (255, 128, 0),  # 6 - Orange
    (128, 0, 255),  # 7 - Purple
    (255, 0, 0),    # 8
    (0, 255, 0),    # 9
    (0, 0, 255),    # 10
    (255, 255, 0),  # 11
    (255, 0, 255),  # 12
    (0, 255, 255),  # 13
    (255, 128, 0),  # 14
    (128, 0, 255),  # 15
]

# Light up all keys
for i in range(NUM_PADS):
    r, g, b = COLORS[i]
    keypad.illuminate(i, r, g, b)
keypad.update()

while True:
    button_states = keypad.get_button_states()
    if button_states:
        for i in range(NUM_PADS):
            if button_states & (1 << i):
                print(f"Key {i} pressed")
                # Dim pressed key to white
                keypad.illuminate(i, 255, 255, 255)
                keypad.update()
    time.sleep(0.05)
```

---

## Step 4 — Stream Deck / OBS Integration

To use as a Stream Deck with OBS:

1. Install the OBS WebSocket plugin on your machine
2. Use [pico-rgbkeypad-streamdeck](https://github.com/BMuuN/pico-rgbkeypad-streamdeck) as a reference
3. Pico sends USB HID keypresses → mapped to OBS hotkeys

Or use **USB HID mode** directly — Pico acts as a keyboard:

```python
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)

# On key press, send a hotkey
kbd.send(Keycode.CONTROL, Keycode.F1)
```

---

## RGB Keypad Pin Map (APA102 LEDs via SPI)

| Function | GPIO |
|----------|------|
| SPI SCK (clock) | GP18 |
| SPI MOSI (data) | GP19 |
| Keypad column select | GP0–GP3 |
| Keypad row read | GP4–GP7 |
| LED CS | GP17 |

> Handled automatically by `picokeypad` library — no manual wiring needed if using the Pimoroni base.

---

## Transfer Files to Pico

Use `mpremote` (recommended):

```bash
pip install mpremote

# Copy main.py to Pico
mpremote connect /dev/cu.usbmodem* cp main.py :main.py

# Open REPL
mpremote connect /dev/cu.usbmodem* repl
```

---

## References

- [Pimoroni RGB Keypad Base](https://shop.pimoroni.com/en-us/products/pico-rgb-keypad-base)
- [pico-rgbkeypad-streamdeck guide](https://github.com/BMuuN/pico-rgbkeypad-streamdeck)
- [Adafruit DIY Pico Mechanical Keyboard](https://learn.adafruit.com/diy-pico-mechanical-keyboard-with-fritzing-circuitpython)
- [MicroPython for Pico 2 W](https://micropython.org/download/RPI_PICO2_W/)
- [CircuitPython for Pico 2 W](https://circuitpython.org/board/raspberry_pi_pico2_w/)
