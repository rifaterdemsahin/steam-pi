# Formula: Flash MicroPython onto Pico 2 W (RP2350)

## Context

Pimoroni does **not** yet have a Pico 2 W (RP2350) build. Use official MicroPython instead.
The `RPI-RP2` / `RP2350` volume may not auto-mount on macOS — use `picotool` to flash directly.

**Date confirmed working:** 2026-02-28
**Board:** Raspberry Pi Pico 2 W (RP2350, serial: 356FBCE36A89FAE4)
**macOS:** Darwin 25.3.0
**Firmware:** MicroPython v1.27.0 (2025-12-09)

---

## Diagnosis: Volume not mounting

The Pico 2 W was detected in USB (`RP2350 Boot`) but **did not mount as a volume** on macOS.

```bash
# Confirmed USB detection:
ioreg -p IOUSB -l -w 0 | grep -A 5 "RP2350"
# Output: "USB Product Name" = "RP2350 Boot"

# Volume NOT present:
ls /Volumes/
# Output: Macintosh HD  (no RP2350 volume)
```

**Root cause:** macOS 25.x does not auto-mount the RP2350 bootloader as a disk.
**Solution:** Use `picotool` to flash directly over USB without needing the volume.

---

## Step 1 — Install picotool

```bash
brew install picotool

# Verify it sees the Pico in BOOTSEL mode:
picotool info
# Expected: "Program Information: none" (empty = no firmware, correct)
```

---

## Step 2 — Download MicroPython UF2 for Pico 2 W

Pimoroni does **not** support RP2350 yet. Use official MicroPython:

```bash
# Latest stable (v1.27.0 as of 2026-02-28):
curl -L "https://micropython.org/resources/firmware/RPI_PICO2_W-20251209-v1.27.0.uf2" \
     -o /tmp/RPI_PICO2_W-v1.27.0.uf2

ls -lh /tmp/RPI_PICO2_W-v1.27.0.uf2
# Expected: ~1.6MB
```

> Always check https://micropython.org/download/RPI_PICO2_W/ for the latest version.

---

## Step 3 — Flash with picotool

Pico must be in BOOTSEL mode (hold BOOTSEL, plug in USB, release).

```bash
picotool load /tmp/RPI_PICO2_W-v1.27.0.uf2 --force && picotool reboot
```

Expected output:
```
Family ID 'rp2350-arm-s' can be downloaded in absolute space:
  00000000->02000000
Loading into Flash:   [==============================]  100%
The device was rebooted into application mode.
```

---

## Step 4 — Verify serial port appears

```bash
sleep 2 && ls /dev/cu.usb*
# Expected: /dev/cu.usbmodem1401  (number may vary)
```

---

## Step 5 — Connect to MicroPython REPL

```bash
screen /dev/cu.usbmodem1401 115200
```

Expected REPL prompt:
```
MicroPython v1.27.0 on 2025-12-09; Raspberry Pi Pico 2 W with RP2350
Type "help()" for more information.
>>>
```

Test it:
```python
>>> print("Steam-Pi online!")
Steam-Pi online!
>>> import machine; machine.freq()
150000000
```

Exit screen: `Ctrl+A`, then `Ctrl+\`, confirm with `y`.

---

## Step 6 — Transfer files with mpremote

```bash
pip3 install mpremote

# Copy main.py
mpremote connect /dev/cu.usbmodem1401 cp main.py :main.py

# List files on Pico
mpremote connect /dev/cu.usbmodem1401 ls
```

---

## ⚠️ Pimoroni `picokeypad` library

The `picokeypad` library is **not included** in official MicroPython — it ships only in the Pimoroni custom build.

**Workaround options:**
1. Install via `mip` (MicroPython package manager):
   ```python
   import mip
   mip.install("github:pimoroni/pimoroni-pico/micropython/modules/picokeypad")
   ```
2. Manually copy `picokeypad.py` from the Pimoroni repo to the Pico
3. Wait for Pimoroni to release a Pico 2 W build

---

## Summary

| Step | Command | Result |
|------|---------|--------|
| Install tool | `brew install picotool` | picotool 2.2.0 |
| Download firmware | `curl micropython.org/...` | 1.6MB UF2 |
| Flash | `picotool load ... --force` | 100% flashed |
| Reboot | `picotool reboot` | App mode |
| Serial port | `ls /dev/cu.usb*` | `/dev/cu.usbmodem1401` |
| REPL | `screen /dev/cu.usbmodem1401 115200` | `>>>` prompt |

**Status: ✅ MicroPython running on Pico 2 W**
