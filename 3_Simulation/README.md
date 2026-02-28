# 🎨 3 — Simulation

> **The "Vision"** — UI mockups and image carousel showing the target state.

---

## Target Vision

A 4×4 RGB keypad sitting on a desk, each key glowing a distinct colour, wired to OBS and gaming actions. Configuration happens entirely in a browser — no code, no terminal.

## Mockups

- `images/` — Screenshots, photos, and design mockups
- `carousel.json` — Image list for the auto-carousel

## Adding Images

1. Add your image to `3_Simulation/images/`
2. Add an entry to `3_Simulation/carousel.json`:
```json
{
  "src": "images/your-image.png",
  "caption": "Description of what this shows"
}
```
3. Commit and push — the carousel updates automatically.
