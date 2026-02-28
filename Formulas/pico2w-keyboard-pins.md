# Formula: Pico 2 W Pin Usage for Keyboard Board

## Is 24 pins normal?

**Yes.** The Raspberry Pi Pico 2 W has **40 physical pins** exposing **26 GPIO pins** (GP0–GP28).
On the Pico 2 W, 4 of those are reserved internally for the wireless chip:

| Pin | Reserved for |
|-----|-------------|
| GP23 | Wireless power control |
| GP24 | Wireless SPI data |
| GP25 | Onboard LED (via wireless chip) |
| GP29 | VSYS voltage sense |

That leaves **~22 freely usable GPIOs** for external use, plus power and ground pins.
Using 24 pins total (GPIO + power/ground) for a keyboard board is expected and normal.

---

## Pico 2 W Full Pinout (40 pins)

```
              USB
         ┌────┤├────┐
GP0   1  │           │  40  VBUS
GP1   2  │           │  39  VSYS
GND   3  │           │  38  GND
GP2   4  │           │  37  3V3_EN
GP3   5  │           │  36  3V3(OUT)
GP4   6  │           │  35  ADC_VREF
GP5   7  │           │  34  GP28 (ADC2)
GND   8  │           │  33  GND
GP6   9  │           │  32  GP27 (ADC1)
GP7  10  │           │  31  GP26 (ADC0)
GP8  11  │           │  30  RUN
GP9  12  │           │  29  GP22
GND  13  │           │  28  GND
GP10 14  │           │  27  GP21
GP11 15  │           │  26  GP20
GP12 16  │           │  25  GP19
GP13 17  │           │  24  GP18
GND  18  │           │  23  GND
GP14 19  │           │  22  GP17
GP15 20  │           │  21  GP16
         └───────────┘
```

---

## How a Keyboard Matrix Uses the Pins

A keyboard matrix wires keys in a grid to reduce pin count:

| Layout | Rows | Columns | Total GPIO pins | Keys supported |
|--------|------|---------|----------------|----------------|
| Numpad | 4 | 4 | 8 | 16 |
| 60% keyboard | 5 | 14 | 19 | 70 |
| TKL (80%) | 6 | 17 | 23 | 102 |
| Full size (100%) | 6 | 18 | 24 | 108 |

**24 pins = rows + columns for a full-size or near-full-size keyboard matrix.**

---

## Recommended Pin Allocation for Keyboard Use

| Purpose | Suggested Pins | Count |
|---------|---------------|-------|
| Row scan (output) | GP0–GP5 | 6 |
| Column read (input) | GP6–GP21 | 16 |
| RGB / LED control | GP22 | 1 |
| I2C (OLED/display) | GP26 (SDA), GP27 (SCL) | 2 |
| Power | VBUS / 3V3 / GND | as needed |

> Avoid GP23, GP24, GP25, GP29 — reserved for wireless on Pico 2 W.

---

## References
- [Pico 2 W Pinout PDF](https://datasheets.raspberrypi.com/picow/pico-2-w-pinout.pdf)
- [Pico 2 W Datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf)
- [Keyboard Matrix with Pico — Raspberry Pi Forums](https://forums.raspberrypi.com/viewtopic.php?t=368265)
