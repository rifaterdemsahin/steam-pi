# Semblance: Pico 2 W Connection Issues

> Semblance = observed symptoms that don't yet have a confirmed fix.

---

## Issue 1 — Pico not detected with original cable

**Symptom:**
- Pico 2 W plugged in via USB
- No `/dev/cu.usb*` serial port appears
- No `RPI-RP2` volume mounted
- `ioreg` shows no Pico-related USB device

**Diagnosis run:**
```bash
ls /dev/cu.usb*          # no matches
ls /Volumes/             # only Macintosh HD
ioreg -p IOUSB -l -w 0  # no Pico/RP2 entry
```

**Suspected cause:** Power-only USB cable (no data wires)

**Action taken:** Swapped to a different cable

---

## Issue 2 — Pico not detected with replacement cable

**Symptom:**
- Different USB cable used
- Still no serial port, no volume, no USB registry entry

**Diagnosis run:**
```bash
ls /dev/cu.usb*          # no matches
ls /Volumes/             # only Macintosh HD
ioreg -p IOUSB -l -w 0  # no output
```

**Status:** Unresolved

---

## Issue 3 — BOOTSEL mode not triggering mass storage

**Symptom:**
- Pico held in BOOTSEL mode while plugging in USB
- Expected: `RPI-RP2` volume appears in `/Volumes/`
- Actual: No volume, no USB device detected at all

**Diagnosis run:**
```bash
ls /Volumes/                          # only Macintosh HD
diskutil list | grep -i "RP\|Pico"   # no output
ioreg -p IOUSB -l -w 0               # no Pico entry
```

**Status:** Unresolved

---

## Next Steps to Investigate

- [ ] Try a different USB port on the MacBook
- [ ] Retry BOOTSEL with stricter timing (hold before plug-in, wait 3s)
- [ ] Run `system_profiler SPUSBDataType` immediately after plugging in to catch transient detection
- [ ] Test Pico on a different machine to rule out board fault
- [ ] Check if Pico 2 W requires a driver on macOS 15+
- [ ] Inspect board for physical damage or bent pins on USB connector

---

## Environment

- Mac: MacBook, macOS Darwin 25.3.0
- Board: Raspberry Pi Pico 2 W (RP2350)
- Expected USB Vendor ID: `0x2E8A`
- Date: 2026-02-28
