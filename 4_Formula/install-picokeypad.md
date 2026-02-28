# Formula: Install picokeypad on Pico 2 W

## Context

The Pimoroni `picokeypad` native module is **compiled into their custom firmware** and is
not available as a pip/mip package. Since Pimoroni has no Pico 2 W (RP2350) build,
we write a **pure Python drop-in replacement** from the C++ source.

**Date confirmed working:** 2026-02-28
**Board:** Raspberry Pi Pico 2 W (RP2350)
**Firmware:** MicroPython v1.27.0

---

## Hardware Pin Map (from Pimoroni C++ source)

| Function | GPIO | Protocol |
|----------|------|----------|
| I2C SDA (button matrix) | GP4 | I2C0 |
| I2C SCL (button matrix) | GP5 | I2C0 |
| SPI CS  (APA102 LEDs)   | GP17 | SPI0 |
| SPI SCK (APA102 LEDs)   | GP18 | SPI0 |
| SPI MOSI (APA102 LEDs)  | GP19 | SPI0 |
| I2C address             | 0x20 | — |
| SPI speed               | 4 MHz | — |

### APA102 LED frame format
```
[0x00 0x00 0x00 0x00]                     ← start frame
[0b111xxxxx  B  G  R] × 16               ← per-LED (xxxxx = brightness 0–31)
[0xFF 0xFF 0xFF 0xFF]                     ← end frame
```

### Button reading (I2C)
```
write 0x00 to addr 0x20
read 2 bytes
states = ~(byte0 | (byte1 << 8)) & 0xFFFF
```

---

## Why mip fails

```bash
mpremote exec "import mip; mip.install('github:pimoroni/...')"
# OSError: -6  ← WiFi not configured, no network access
```

**Fix:** Copy the module directly from Mac using `mpremote cp`.

---

## Step 1 — Create the pure Python module

Save as `picokeypad.py` (see `5_Symbols/picokeypad.py` in this repo).

The module exposes the same API as the native Pimoroni module:

| Function | Description |
|----------|-------------|
| `init()` | Initialise SPI + I2C |
| `get_num_pads()` | Returns 16 |
| `set_brightness(0.0–1.0)` | Global LED brightness |
| `illuminate(i, r, g, b)` | Set key i colour |
| `update()` | Push LED data via SPI |
| `clear()` | Turn off all LEDs |
| `get_button_states()` | 16-bit bitmask of pressed keys |

---

## Step 2 — Copy to Pico

```bash
# Create lib directory on Pico
mpremote connect /dev/cu.usbmodem1401 mkdir lib

# Copy module
mpremote connect /dev/cu.usbmodem1401 cp picokeypad.py :lib/picokeypad.py

# Verify
mpremote connect /dev/cu.usbmodem1401 ls lib
```

---

## Step 3 — Test

```bash
mpremote connect /dev/cu.usbmodem1401 exec "
import picokeypad as keypad
keypad.init()
keypad.set_brightness(1.0)
keypad.illuminate(0,  255, 0,   0)    # key 0  → red
keypad.illuminate(5,  0,   255, 0)    # key 5  → green
keypad.illuminate(10, 0,   0,   255)  # key 10 → blue
keypad.illuminate(15, 255, 255, 255)  # key 15 → white
keypad.update()
print('Keys lit:', hex(0b1000000000100001))
print('Button states:', hex(keypad.get_button_states()))
"
```

**Expected output:**
```
Keys lit: 0x8021
Button states: 0x0   ← 0x0 = no keys pressed
```

**Expected on hardware:** Keys 0, 5, 10, 15 glow red/green/blue/white ✅

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `ImportError: no module named 'picokeypad'` | Not in `/lib` | Re-run `mpremote cp` step |
| `OSError` on `get_button_states()` | I2C wiring issue or keypad not attached | Check SDA=GP4, SCL=GP5 |
| LEDs don't light | SPI wiring issue | Check SCK=GP18, MOSI=GP19, CS=GP17 |
| All buttons read as pressed | I2C address wrong | Confirm 0x20 with `i2c.scan()` |

Scan I2C to verify address:
```python
from machine import I2C, Pin
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400_000)
print([hex(a) for a in i2c.scan()])
# Expected: ['0x20']
```

---

## Status: ✅ Working on Pico 2 W with MicroPython v1.27.0
