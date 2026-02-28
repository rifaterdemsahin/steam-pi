# CLAUDE.md — steam-pi

## Project Overview
RGB macro keyboard (Stream Deck style) built with a Raspberry Pi Pico 2 W and Pimoroni RGB Keypad Base (4×4, 16 APA102 keys).

## Hardware
- **Board:** Raspberry Pi Pico 2 W (RP2350 chip, onboard WiFi/BT)
- **Keypad:** Pimoroni Pico RGB Keypad Base — 16 silicone keys, APA102 RGB LEDs
- **Connection:** USB to MacBook (must be a data-capable cable)

## Reserved GPIO pins (do not use)
| Pin | Used for |
|-----|----------|
| GP23 | Wireless power control |
| GP24 | Wireless SPI data |
| GP25 | Onboard LED (via wireless chip) |
| GP29 | VSYS voltage sense |

## Firmware
- **MicroPython:** Pimoroni custom build (includes `picokeypad` library)
  - Download: https://github.com/pimoroni/pimoroni-pico/releases
  - File: `pimoroni-pico2w-*.uf2`
- **Flash method:** BOOTSEL mode (hold BOOTSEL, plug USB, release after 3s)

## Key files
| File | Purpose |
|------|---------|
| `setup_keyboard.html` | Web UI to configure key colors, labels, actions; exports MicroPython |
| `Formulas/connect-pico2w-mac.md` | How to connect Pico 2 W to macOS |
| `Formulas/pico2w-keyboard-pins.md` | Pin layout and keyboard matrix reference |
| `Formulas/setup-pico-rgb-keyboard.md` | Full step-by-step setup guide |
| `Semblance/pico2w-connection-issues.md` | Unresolved connection issues log |

## Workflow
1. Configure keys in `setup_keyboard.html` — set colors, icons, actions
2. Copy exported MicroPython from the page
3. Save as `main.py` and deploy to Pico with `mpremote`

```bash
pip install mpremote
mpremote connect /dev/cu.usbmodem* cp main.py :main.py
```

## Connecting to Pico REPL
```bash
ls /dev/cu.usb*                        # find port
screen /dev/cu.usbmodem* 115200        # open REPL
# exit: Ctrl+A then Ctrl+\, confirm y
```

## Folder conventions
- `Formulas/` — step-by-step how-to guides (working solutions)
- `Semblance/` — observed issues not yet resolved (bug/issue log)
