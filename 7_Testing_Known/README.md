# ✅ 7 — Testing Known

> **The "Proof"** — Validation against `1_Real_Unknown` objectives, testing checklists, and outcome confirmation.

---

## Testing Checklist

### Hardware Tests

- [ ] Pico 2 W detected as `/dev/cu.usbmodem*` on macOS
- [ ] `RPI-RP2` volume appears in BOOTSEL mode
- [ ] MicroPython REPL accessible (`>>>` prompt)
- [ ] `import picokeypad` succeeds in REPL
- [ ] All 16 RGB keys illuminate
- [ ] Each key's correct color matches `KEY_CONFIG`

### Software Tests

- [ ] `main.py` deploys without errors via mpremote
- [ ] Key press triggers correct action (hotkey/OBS/text)
- [ ] USB HID keypress received by macOS
- [ ] OBS WebSocket command acknowledged

### Web UI Tests

- [ ] `index.html` loads on GitHub Pages
- [ ] Navigation renders on all 7 section pages
- [ ] Debug menu toggles with cookie persistence
- [ ] Search returns correct autocomplete results
- [ ] `markdown_renderer.html` renders `.md` files
- [ ] `setup_keyboard.html` exports valid MicroPython
- [ ] Carousel loads in `3_Simulation/index.html`
- [ ] Mobile layout correct on 375px viewport

### OKR Validation

See `1_Real_Unknown/okrs.md` for current status against all objectives.
