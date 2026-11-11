# zigbee-c6-dongle

Board revision: v1.0

A small USB Zigbee coordinator stick built around the Espressif ESP32-C6-MINI-1U-H4 module. It plugs straight into a USB-A port on a Home Assistant host (a Raspberry Pi, for example) and gives it a Zigbee radio with an external antenna connector.

## Purpose

The goal is an open, hand-solderable Zigbee coordinator for Home Assistant that does not depend on a vendor dongle. Every SMD passive is 0603 or larger, all parts are available from DigiKey, and the board is a 4-layer design sized for JLCPCB's standard process.

## Hardware

| Item | Detail |
| --- | --- |
| Radio / MCU | ESP32-C6-MINI-1U-H4 (802.15.4 + Wi-Fi 6 + BLE, U.FL antenna connector) |
| USB | Male USB-A plug, ESP32-C6 native USB Serial/JTAG on D+/D- |
| Protection | 500 mA resettable fuse (MF-NSMF050-2) and USBLC6-2SC6 ESD array |
| Power | AP2112K-3.3 3.3 V, 600 mA LDO (pin-compatible with TLV75733P) |
| Expansion | Two 4-pin JST-SH connectors: I2C (Qwiic / STEMMA QT pinout) and UART0 |
| Controls | BOOT and RST buttons, power and status LEDs |
| Board | 58.25 mm x 20.75 mm, 4 layers (signal / GND / 3V3 / signal), two 2.0 mm case indexing holes |

The board also has an unpopulated footprint for an MCP2221A USB-to-UART bridge. It is a fallback in case the native USB port is not suitable: fit U4 with its support parts and move the two USB series resistors from R3/R4 to R10/R11.

Two normally-open solder jumpers, JP1 and JP2, can also wire the bridge straight to the UART connector so the stick works as a plain 3.3 V USB-to-serial adapter. That mode needs the bridge fitted and the ESP32-C6 held in reset or left unprogrammed.

## Software

The dongle itself runs [esp-coordinator](https://github.com/aliciusschroeder/esp-coordinator), a Zigbee coordinator firmware for the ESP32-C6 that speaks the ZBOSS NCP serial protocol over USB.

On the Home Assistant side there are two options:

- **ZHA** with the [zha-zboss-esp](https://github.com/tostmann/zha-zboss-esp) adapter (installed through HACS). This is the primary target.
- **Zigbee2MQTT** with its `zboss` adapter, as the fallback.

The firmware is flashed over the same USB port. Hold BOOT while tapping RST to enter the ROM bootloader.

## Repository layout

```
hardware/zigbee-c6-dongle/      KiCad project (schematic, PCB, library tables)
hardware/zigbee-c6-dongle/production/   JLCPCB gerbers, BOM and placement files
documentation/assets/custom/    Project symbol and footprint libraries
documentation/assets/           Vendor CAD downloads and 3D models (STEP)
documentation/datasheet/        Component datasheets
documentation/exports/          PDF plots of the schematic and layout
```

## Opening the project

The project was drawn in KiCad 10. Clone the repository and open `hardware/zigbee-c6-dongle/zigbee-c6-dongle.kicad_pro`. No library setup is needed:

- The `custom` symbol and footprint libraries are registered in the project's own `sym-lib-table` and `fp-lib-table` using `${KIPRJMOD}`-relative paths.
- Vendor 3D models are referenced relative to the project, and the remaining models come from the standard KiCad library (`${KICAD10_3DMODEL_DIR}`).
- Passives, LEDs, switches and the indexing holes use the stock KiCad libraries.

After opening the PCB, press `B` to refill the copper zones before running DRC or exporting fabrication files.

## Third-party files

The vendor symbols, footprints and STEP models under `documentation/assets/` belong to their respective manufacturers and CAD providers. Licence notes are kept alongside the files where the source supplied them.
