# 🎯 1 — Real Unknown

> **The "Why"** — Problem definitions, OKRs, and the core questions.

---

## Problem Statement

I want to use a Raspberry Pi Pico 2 W as a dedicated **RGB macro keyboard / Steam Deck companion** that:
- Controls OBS scenes, mute/unmute, recording start/stop
- Acts as a gaming macro pad with configurable RGB per key
- Can be configured via a web UI without writing code

The unknown: Can a $6 microcontroller replace a $150 Elgato Stream Deck while adding wireless capability?

---

## OKRs

### Objective 1 — Physical Hardware Working
| Key Result | Target | Status |
|---|---|---|
| Pico 2 W detected by macOS | USB serial port visible | 🔴 In progress |
| MicroPython REPL accessible | `>>>` prompt in screen | 🔴 In progress |
| RGB keys illuminate correctly | All 16 keys light up | 🔴 Pending |

### Objective 2 — Keyboard Functionality
| Key Result | Target | Status |
|---|---|---|
| Keys send USB HID input | Hotkey received by host | 🔴 Pending |
| OBS integration working | Scene switch via keypress | 🔴 Pending |
| Web config UI usable | Export + deploy in < 2 min | 🟡 Partial (UI done) |

### Objective 3 — Documentation Complete
| Key Result | Target | Status |
|---|---|---|
| Setup reproducible by anyone | Zero prior knowledge needed | 🟡 In progress |
| All 7 stages documented | Each folder has README | 🟡 In progress |

---

## Core Questions

1. Why does Pico 2 W not show up via USB on macOS with two different cables?
2. Is BOOTSEL mode working correctly on this specific board?
3. Can the Pimoroni RGB keypad base work with the Pico 2 W (RP2350) vs the original Pico (RP2040)?
4. What latency does USB HID have vs Bluetooth HID for gaming use?
5. Can the wireless capability be used for OBS WebSocket control over WiFi?

---

## Success Definition

**Done** = A Pico 2 W with 16 RGB keys sits on a desk, keys are configured via browser UI, and pressing a key either sends a hotkey to the computer or triggers an OBS action over WiFi — all without touching any code.
