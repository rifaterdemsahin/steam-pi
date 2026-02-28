# OKR Tracker — Steam-Pi

## Objective 1 — Physical Hardware Working
| Key Result | Target | Status |
|---|---|---|
| Pico 2 W detected by macOS | USB serial port visible | 🟢 Done — `/dev/cu.usbmodem1401` |
| MicroPython REPL accessible | `>>>` prompt in screen | 🟢 Done — v1.27.0 flashed via picotool |
| RGB keys illuminate correctly | All 16 keys light up | 🟢 Done — pure Python picokeypad installed, keys 0/5/10/15 lit |

**Resolved:** New cable + `picotool load` bypassed the macOS volume mount issue.
See `4_Formula/flash-micropython-pico2w.md` for full steps.

## Objective 2 — Keyboard Functionality
| Key Result | Target | Status |
|---|---|---|
| Keys send USB HID input | Hotkey received by host | 🔴 Pending |
| OBS integration working | Scene switch via keypress | 🔴 Pending |
| Web config UI functional | Export + deploy < 2 min | 🟢 Done |

## Objective 3 — Documentation Complete
| Key Result | Target | Status |
|---|---|---|
| Setup reproducible | Zero prior knowledge needed | 🟡 In Progress |
| All 7 stages documented | Each folder has README | 🟡 In Progress |
| GitHub Pages live | Public URL accessible | 🟡 In Progress |
