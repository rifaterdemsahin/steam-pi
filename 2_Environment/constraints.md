# Constraints — Steam-Pi

## Hardware Constraints

| Constraint | Detail |
|---|---|
| GPIO23-25, GP29 reserved | Used by wireless chip on Pico 2 W — do not use for keyboard |
| SPI pins fixed | RGB keypad uses GP18 (SCK), GP19 (MOSI), GP17 (CS) |
| USB power draw | Max 500mA from USB — RGB at full brightness may need external power |
| RP2350 vs RP2040 | Pico 2 W uses RP2350; some older libraries target RP2040 only |

## Software Constraints

| Constraint | Detail |
|---|---|
| Static site only | GitHub Pages serves static files — no server-side code |
| No build step | Vanilla HTML/CSS/JS — no npm, no webpack |
| Relative paths required | GitHub Pages base URL includes repo name — use BASE_PATH |
| Pimoroni UF2 required | Standard MicroPython lacks `picokeypad` — must use Pimoroni build |

## Known Gotchas

- `adafruit_hid` must be installed separately even with Pimoroni firmware
- macOS may not auto-mount `RPI-RP2` — check Disk Utility if volume doesn't appear
- Screen session can orphan — run `screen -list` and `screen -X quit` to clean up
- Pico 2 W (RP2350) BOOTSEL button may need to be held longer than RP2040
