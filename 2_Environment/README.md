# 🌍 2 — Environment

> **The "Context"** — Roadmaps, constraints, and setup guides.

---

## Hardware Environment

- **Board:** Raspberry Pi Pico 2 W (RP2350, 264KB SRAM, 2MB flash, WiFi + BT)
- **Keypad:** Pimoroni RGB Keypad Base (4×4 APA102 LEDs, SPI interface)
- **Host:** MacBook, macOS Darwin 25.3.0
- **Connection:** USB-C to USB-A/C cable (must support data, not power-only)

## Software Stack

| Tool | Version | Purpose |
|------|---------|---------|
| MicroPython | Pimoroni custom build | Firmware for Pico 2 W |
| picokeypad | Bundled in Pimoroni UF2 | RGB keypad driver |
| mpremote | latest via pip | File transfer + REPL |
| screen / tio | macOS built-in | Serial terminal |
| GitHub Pages | N/A | Static site hosting |

## AI Stack (Future)

| Tool | Config | Purpose |
|------|--------|---------|
| Ollama | `nomic-embed-text` (4096 dims) | Local embeddings |
| Qdrant | `localhost:6333` | Vector search |

## Constraints

- No build step — pure static HTML/CSS/JS
- No frameworks — vanilla JS only
- GitHub Pages compatible — all paths must be relative
- Pico 2 W GPIO23, GP24, GP25, GP29 reserved for wireless chip

## Roadmap

1. ✅ Repository + framework structure created
2. ✅ Web keyboard config UI built
3. 🔴 Pico 2 W USB connection unblocked
4. 🔴 MicroPython flashed
5. 🔴 RGB keys working
6. 🔴 USB HID hotkeys working
7. 🔴 OBS WiFi integration
