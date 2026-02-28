"""
Steam-Pi — main.py
Pico 2 W RGB Keyboard Controller

Flash to Pico 2 W using:
  mpremote connect /dev/cu.usbmodem* cp main.py :main.py

Requirements (Pimoroni MicroPython UF2):
  - picokeypad
  - usb_hid (via adafruit_hid)
"""

import picokeypad as keypad
import usb_hid
import time

try:
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
    from adafruit_hid.keycode import Keycode
    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    HID_AVAILABLE = True
except ImportError:
    HID_AVAILABLE = False
    print("adafruit_hid not found — HID disabled, using print mode")

# ── Init ───────────────────────────────────────────────────────────────────
keypad.init()
keypad.set_brightness(1.0)
NUM_KEYS = keypad.get_num_pads()  # 16

# ── Key configuration ──────────────────────────────────────────────────────
# Edit setup_keyboard.html in a browser then paste the generated config here.
# Format: (R, G, B, label, action_type, action_data)

KEY_CONFIG = [
    (255,   0,   0, "Scene 1",   "obs",    "obs:scene:1"),       # 0
    (  0, 255,   0, "Scene 2",   "obs",    "obs:scene:2"),       # 1
    (  0,   0, 255, "Scene 3",   "obs",    "obs:scene:3"),       # 2
    (255, 255,   0, "Scene 4",   "obs",    "obs:scene:4"),       # 3
    (255,   0, 255, "Stream",    "obs",    "obs:stream:toggle"), # 4
    (  0, 255, 255, "Record",    "obs",    "obs:record:toggle"), # 5
    (255, 128,   0, "Mute Mic",  "obs",    "obs:mute:mic"),      # 6
    (128,   0, 255, "Screenshot","obs",    "obs:screenshot"),    # 7
    (255,  50,  50, "F13",       "hotkey", [Keycode.F13] if HID_AVAILABLE else []), # 8
    ( 50, 255,  50, "F14",       "hotkey", [Keycode.F14] if HID_AVAILABLE else []), # 9
    ( 50,  50, 255, "F15",       "hotkey", [Keycode.F15] if HID_AVAILABLE else []), # 10
    (200, 200,   0, "F16",       "hotkey", [Keycode.F16] if HID_AVAILABLE else []), # 11
    (200,   0, 200, "F17",       "hotkey", [Keycode.F17] if HID_AVAILABLE else []), # 12
    (  0, 200, 200, "F18",       "hotkey", [Keycode.F18] if HID_AVAILABLE else []), # 13
    (255, 200, 100, "F19",       "hotkey", [Keycode.F19] if HID_AVAILABLE else []), # 14
    (100, 100, 100, "F20",       "hotkey", [Keycode.F20] if HID_AVAILABLE else []), # 15
]

# ── Light up keys ──────────────────────────────────────────────────────────
for i, cfg in enumerate(KEY_CONFIG):
    r, g, b = cfg[0], cfg[1], cfg[2]
    keypad.illuminate(i, r, g, b)
keypad.update()

print("Steam-Pi keyboard ready —", NUM_KEYS, "keys active")

# ── Action handlers ────────────────────────────────────────────────────────
def handle_obs(action):
    """Send OBS action over serial (host-side script reads this)."""
    print(f"OBS:{action}")

def handle_hotkey(keycodes):
    """Send HID keypress."""
    if not HID_AVAILABLE or not keycodes:
        return
    try:
        kbd.send(*keycodes)
    except Exception as e:
        print("HID error:", e)

def on_press(i):
    """Called when key i is pressed."""
    if i >= len(KEY_CONFIG):
        return
    cfg = KEY_CONFIG[i]
    label, action_type, action_data = cfg[3], cfg[4], cfg[5]
    print(f"Key {i}: {label}")

    # Flash white on press
    keypad.illuminate(i, 255, 255, 255)
    keypad.update()
    time.sleep(0.05)
    keypad.illuminate(i, cfg[0], cfg[1], cfg[2])
    keypad.update()

    if action_type == "hotkey":
        handle_hotkey(action_data)
    elif action_type == "obs":
        handle_obs(action_data)
    elif action_type == "text" and HID_AVAILABLE:
        layout.write(action_data)

# ── Main loop ──────────────────────────────────────────────────────────────
prev_state = 0
while True:
    state = keypad.get_button_states()
    if state != prev_state:
        for i in range(NUM_KEYS):
            if (state & (1 << i)) and not (prev_state & (1 << i)):
                on_press(i)
        prev_state = state
    time.sleep(0.02)
