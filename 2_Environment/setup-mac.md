# Mac Setup Guide — Pico 2 W Development

## Prerequisites
- macOS (tested on Darwin 25.3.0)
- Python 3.x (`python3 --version`)
- Homebrew (optional but recommended)

## Step 1 — Install mpremote
```bash
pip3 install mpremote
```

## Step 2 — Find the Pico serial port
```bash
ls /dev/cu.usb*
# Expected: /dev/cu.usbmodem101 (or similar)
```

## Step 3 — Open MicroPython REPL
```bash
screen /dev/cu.usbmodem* 115200
# Exit: Ctrl+A, then Ctrl+\, confirm y
```

Or with mpremote:
```bash
mpremote connect /dev/cu.usbmodem* repl
# Exit: Ctrl+X
```

## Step 4 — Transfer files
```bash
# Copy a file to Pico
mpremote connect /dev/cu.usbmodem* cp main.py :main.py

# List files on Pico
mpremote connect /dev/cu.usbmodem* ls

# Run a file without saving
mpremote connect /dev/cu.usbmodem* run main.py
```

## Step 5 — Install tio (better serial terminal)
```bash
brew install tio
tio /dev/cu.usbmodem* -b 115200
# Exit: Ctrl+T, then Q
```
