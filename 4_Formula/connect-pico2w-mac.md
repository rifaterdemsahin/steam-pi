# Formula: Connect Pico 2 W to MacBook

## Problem
Pico 2 W is connected via USB but not detected by macOS — no serial port, no volume mounted.

---

## Diagnosis

Run these commands to check device state:

```bash
# Check for serial ports
ls /dev/cu.usb* /dev/tty.usb*

# Check for mounted volumes (bootloader mode)
ls /Volumes/

# Check USB registry
ioreg -p IOUSB -l -w 0 | grep -E "idVendor|idProduct|USB Product Name"
```

**Expected outputs:**
| State | Output |
|---|---|
| MicroPython running | `/dev/cu.usbmodem*` appears |
| Bootloader mode | `RPI-RP2` appears in `/Volumes/` |
| Not detected | None of the above |

---

## Root Causes

1. **Power-only USB cable** — no data wires, most common cause
2. **No firmware flashed** — Pico never had MicroPython installed
3. **Loose connection** — cable or port issue

---

## Formula

### Step 1 — Rule out cable issue
Swap to a USB cable confirmed to carry data (e.g., one used for phone file transfer).

### Step 2 — Enter BOOTSEL (bootloader) mode
1. Unplug the Pico from USB
2. Hold the **BOOTSEL** button on the board
3. While holding BOOTSEL, plug USB back in
4. Release BOOTSEL after 2-3 seconds

Verify:
```bash
ls /Volumes/
# Expected: RPI-RP2
```

### Step 3 — Flash MicroPython
1. Download the UF2 firmware:
   - https://micropython.org/download/RPI_PICO2_W/
2. Drag the `.uf2` file onto the `RPI-RP2` volume
3. The Pico reboots automatically

### Step 4 — Connect via serial
After flashing, unplug and replug the Pico (no BOOTSEL needed).

```bash
# Find the port
ls /dev/cu.usb*

# Connect (replace with actual port name)
screen /dev/cu.usbmodem* 115200
```

You should see the MicroPython REPL:
```
MicroPython vX.X.X on YYYY-MM-DD; Raspberry Pi Pico 2 W
>>>
```

To exit `screen`: press `Ctrl+A` then `Ctrl+\`, confirm with `y`.

---

## Quick Reference

| Command | Purpose |
|---|---|
| `ls /dev/cu.usb*` | Find Pico serial port |
| `ls /Volumes/` | Check bootloader mount |
| `screen /dev/cu.usbmodem* 115200` | Open REPL |
| `Ctrl+A`, `Ctrl+\` | Exit screen |

---

## Notes
- Pico 2 W vendor ID: `0x2E8A`
- Default baud rate for MicroPython: `115200`
- BOOTSEL mode is safe — it does not erase existing firmware
