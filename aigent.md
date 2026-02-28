# aigent.md — AI Agent Rules for Steam-Pi

## Project Context
Steam-Pi is a self-learning documentation system for building a Raspberry Pi Pico 2 W RGB macro keyboard (Stream Deck style), following the 7-stage Unknown → Proven framework.

## Folder Framework

| Folder | Purpose | Stage |
|--------|---------|-------|
| `1_Real_Unknown/` | Problem definitions, OKRs, "Why" | Unknown |
| `2_Environment/` | Setup guides, constraints, toolchain | Context |
| `3_Simulation/` | UI mockups, carousel, "Vision" | Vision |
| `4_Formula/` | Step-by-step guides, research, "Recipe" | Recipe |
| `5_Symbols/` | Source code, implementation | Reality |
| `6_Semblance/` | Error logs, workarounds, "Scars" | Scars |
| `7_Testing_Known/` | Validation, checklists, "Proof" | Proven |

## AI Behaviour Rules

### Always
- Read CLAUDE.md for hardware and workflow context
- Use `4_Formula/` for any new how-to guide
- Use `6_Semblance/` for any new error or issue log
- Use `7_Testing_Known/` for any new validation step
- Commit and push after every significant change
- Use the shared nav (nav.json + js/nav.js) for any new HTML page
- Include `window.BASE_PATH` and load `js/nav.js` in every page

### Never
- Create docs outside the 7-folder structure
- Hardcode navigation — always read from nav.json
- Skip the `<div id="nav-container">` in HTML pages
- Use absolute paths for internal links (use BASE_PATH-relative paths)

### When adding a new page
1. Add it to `contentMenu` in nav.json
2. Add it to `searchIndex` in nav.json
3. Include the standard nav snippet:
   ```html
   <div id="nav-container"></div>
   <!-- ... page content ... -->
   <script>window.BASE_PATH = '../';</script>  <!-- or './' for root -->
   <script src="../js/nav.js"></script>        <!-- adjust depth -->
   ```
4. Link `css/style.css`

### When adding a new markdown guide
1. Place in appropriate folder (4_Formula for guides, 6_Semblance for issues)
2. Add to searchIndex in nav.json
3. Access via markdown_renderer.html?file=path/to/file.md

## Lifecycle
- Move obsolete files to `_obsolete/` subfolder in their respective directory
- Tag issues in 6_Semblance with status: Resolved / Unresolved / Workaround

## Tech Stack
- Static HTML/CSS/JS — no build step, deploys via GitHub Pages
- MicroPython on Pico 2 W (RP2350)
- Pimoroni RGB Keypad Base (APA102 LEDs, picokeypad library)
- marked.js for markdown rendering
- PrismJS for syntax highlighting
