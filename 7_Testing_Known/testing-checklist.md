# Testing Checklist — Steam-Pi

> Validate every objective from `1_Real_Unknown` before marking the project proven.

## Phase 1 — Hardware

- [ ] Pico 2 W USB cable carries data (test with `ls /dev/cu.usb*`)
- [ ] BOOTSEL mode mounts `RPI-RP2` volume
- [ ] Pimoroni MicroPython UF2 flashed successfully
- [ ] `screen /dev/cu.usbmodem* 115200` opens REPL
- [ ] `import picokeypad` works in REPL
- [ ] `keypad.illuminate(0, 255, 0, 0); keypad.update()` lights key 0 red

## Phase 2 — Firmware

- [ ] `main.py` uploads via `mpremote cp main.py :main.py`
- [ ] Pico auto-runs `main.py` on power-up
- [ ] All 16 keys show correct colors on boot
- [ ] Pressing key 0 prints `Key 0: Scene 1` in REPL
- [ ] Pressing key 0 triggers OBS scene switch (if OBS WebSocket active)

## Phase 3 — HID

- [ ] `adafruit_hid` installed on Pico
- [ ] Pressing key 8 sends F13 to macOS
- [ ] No phantom keypresses or stuck keys

## Phase 4 — Web UI

- [ ] GitHub Pages URL loads `index.html`
- [ ] All 7 nav links functional
- [ ] Debug button toggles framework menu
- [ ] Debug state persists on page reload (cookie)
- [ ] Search finds "RGB" and shows results
- [ ] `markdown_renderer.html?file=4_Formula/connect-pico2w-mac.md` renders correctly
- [ ] `setup_keyboard.html` → configure key 0 → click Apply → MicroPython export updates

## Phase 5 — OKR Sign-off

Review `1_Real_Unknown/okrs.md` — all items should be 🟢 before final sign-off.
