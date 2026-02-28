"""
picokeypad.py — Pure Python drop-in for Pimoroni picokeypad
Runs on standard MicroPython (no Pimoroni custom firmware needed).

Hardware: Pimoroni Pico RGB Keypad Base
  SPI  → APA102 LEDs  — SCK=GP18, MOSI=GP19, CS=GP17
  I2C  → Button matrix — SDA=GP4,  SCL=GP5,  addr=0x20

Usage (identical to the Pimoroni native module):
  import picokeypad as keypad
  keypad.init()
  keypad.set_brightness(1.0)
  keypad.illuminate(0, 255, 0, 0)
  keypad.update()
  states = keypad.get_button_states()  # 16-bit bitmask
"""

from machine import SPI, I2C, Pin

# ── Constants ──────────────────────────────────────────────────
NUM_PADS         = 16
KEYPAD_I2C_ADDR  = 0x20
DEFAULT_BRIGHTNESS = 0.5

# ── Module-level state ─────────────────────────────────────────
_spi        = None
_i2c        = None
_cs         = None
_buf        = None   # bytearray: start(4) + leds(16×4) + end(4)
_brightness = DEFAULT_BRIGHTNESS


def init():
    """Initialise SPI (LEDs) and I2C (buttons). Call once at startup."""
    global _spi, _i2c, _cs, _buf

    # APA102 LEDs via SPI0
    _spi = SPI(0, baudrate=4_000_000, sck=Pin(18), mosi=Pin(19))
    _cs  = Pin(17, Pin.OUT, value=1)

    # Button matrix via I2C0
    _i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400_000)

    # APA102 frame: [0x00×4] + [led×16] + [0xFF×4]
    _buf = bytearray(4 + NUM_PADS * 4 + 4)
    _buf[-4:] = b'\xff\xff\xff\xff'

    set_brightness(DEFAULT_BRIGHTNESS)
    update()


def get_num_pads():
    """Return number of keys (always 16)."""
    return NUM_PADS


def set_brightness(brightness):
    """Set global LED brightness (0.0–1.0)."""
    global _brightness
    brightness = max(0.0, min(1.0, float(brightness)))
    _brightness = brightness
    frame = 0b11100000 | int(brightness * 0b11111)
    for i in range(NUM_PADS):
        _buf[4 + i * 4] = frame


def illuminate(index, r, g, b):
    """
    Set LED at index (0–15) to RGB colour.
    APA102 wire order is BGR, this function accepts standard RGB.
    """
    if index < 0 or index >= NUM_PADS:
        return
    off = 4 + index * 4
    _buf[off + 1] = int(b)
    _buf[off + 2] = int(g)
    _buf[off + 3] = int(r)


def update():
    """Push LED buffer to the keypad via SPI."""
    _cs.value(0)
    _spi.write(_buf)
    _cs.value(1)


def clear():
    """Turn off all LEDs."""
    for i in range(NUM_PADS):
        illuminate(i, 0, 0, 0)
    update()


def get_button_states():
    """
    Return a 16-bit bitmask of currently pressed keys.
    Bit 0 = key 0, bit 15 = key 15. 1 = pressed.
    Returns 0 on I2C error.
    """
    try:
        _i2c.writeto(KEYPAD_I2C_ADDR, b'\x00')
        data = _i2c.readfrom(KEYPAD_I2C_ADDR, 2)
        return (~(data[0] | (data[1] << 8))) & 0xFFFF
    except OSError:
        return 0
