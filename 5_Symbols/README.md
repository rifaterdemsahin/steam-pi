# 💻 5 — Symbols

> **The "Reality"** — Core source code and implementation.

---

## Files

| File | Description |
|------|-------------|
| `main.py` | MicroPython entry point for Pico 2 W — RGB keys + HID + OBS |

## Deploy

```bash
# Transfer to Pico
mpremote connect /dev/cu.usbmodem* cp main.py :main.py

# Verify
mpremote connect /dev/cu.usbmodem* ls
```

## Customise

Use `setup_keyboard.html` in a browser to configure keys visually, then paste the exported MicroPython config into `KEY_CONFIG` in `main.py`.
