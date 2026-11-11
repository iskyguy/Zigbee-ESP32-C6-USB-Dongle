# zigbee-c6-dongle

Board revision: v1.0

A small USB Zigbee coordinator stick built around the Espressif ESP32-C6-MINI-1U-H4 module. It plugs straight into a USB-A port on a Home Assistant host (a Raspberry Pi, for example) and gives it a Zigbee radio with an external antenna connector.

## Purpose

The goal is an open, hand-solderable Zigbee coordinator for Home Assistant that does not depend on a vendor dongle. Every SMD passive is 0603 or larger, all parts are available from DigiKey, and the board is a 4-layer design set up for OSH Park's 4-layer service.

## Hardware

| Item | Detail |
| --- | --- |
| Radio / MCU | ESP32-C6-MINI-1U-H4 (802.15.4 + Wi-Fi 6 + BLE, U.FL antenna connector) |
| USB | Male USB-A plug, ESP32-C6 native USB Serial/JTAG on D+/D- |
| Protection | 500 mA resettable fuse (MF-NSMF050-2) and USBLC6-2SC6 ESD array |
| Power | AP2112K-3.3 3.3 V, 600 mA LDO (pin-compatible with TLV75733P) |
| Expansion | Two 4-pin JST-SH connectors: I2C (Qwiic / STEMMA QT pinout) and UART0 |
| Controls | BOOT and RST buttons, power and status LEDs |
| Board | 58.25 mm x 20.75 mm, 4 layers (signal / GND / 3V3 / signal), 1.6 mm FR408-HR, ENIG, two 2.0 mm case indexing holes |

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
hardware/zigbee-c6-dongle/production/oshpark/   OSH Park 4-layer gerbers and drill file
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

## Ordering from OSH Park

The board's design rules and stackup match OSH Park's 4-layer prototype service, and DRC passes against them. There are two ways to order:

- **Upload the KiCad board.** OSH Park accepts `zigbee-c6-dongle.kicad_pcb` directly and generates the Gerbers itself. It does not refill zones, so press `B` and save before uploading if you have changed anything. The plot settings stored in the board (the layers listed below) are used.
- **Upload the Gerber zip.** `production/oshpark/Zigbee_C6_Dongle_v1.0_OSHPark.zip` holds Gerber X2 files for F.Cu, In1.Cu (`.G2L`), In2.Cu (`.G3L`), B.Cu, both masks, silkscreens and pastes, the Edge.Cuts outline (`.GKO`), a job file, and one Excellon drill file (metric, absolute origin, decimal format, alternate drill mode for the USB plug slots). To regenerate it, use **File > Plot** (the settings are saved in the board and write to `production/oshpark/`) and **Generate Drill Files** with the options above.

Design rules (Board Setup > Constraints), from OSH Park's 4-layer specification:

| Rule | Value |
| --- | --- |
| Minimum clearance, track width and connection width | 0.127 mm (5 mil) |
| Minimum via diameter | 0.4572 mm (18 mil) |
| Minimum annular ring | 0.1016 mm (4 mil) |
| Minimum through hole | 0.254 mm (10 mil) |
| Hole to copper clearance | 0.254 mm (10 mil, OSH Park's plated drill to internal copper limit) |
| Hole to hole clearance | 0.127 mm (5 mil) |
| Copper to board edge | 0.381 mm (15 mil) |
| Solder mask expansion / minimum web | 0.0508 mm (2 mil) / 0.1016 mm (4 mil) |
| Minimum silkscreen text thickness | 0.127 mm (5 mil) |

The routing itself is unchanged and stays well above these limits: 0.2 mm minimum track and clearance, and 0.6 mm vias with 0.3 mm drills. OSH Park offers no blind, buried or via-in-pad vias, and the board uses none.

The stackup in Board Setup follows OSH Park's published 4-layer build: 1 oz outer copper (0.0432 mm), 0.1999 mm FR408-HR 2113 prepreg, 0.5 oz inner copper (0.0175 mm), and a 0.9906 mm FR408-HR core, with Dk 3.61, ENIG finish, purple mask and white silkscreen. OSH Park quotes the finished board as 1.6 mm nominal. These values only matter for impedance calculations, since OSH Park always builds to its own stackup.

At OSH Park's $10 per square inch the 58.25 mm x 20.75 mm board is about 1.87 square inches, so a set of three costs about $19.

## Third-party files

The vendor symbols, footprints and STEP models under `documentation/assets/` belong to their respective manufacturers and CAD providers. Licence notes are kept alongside the files where the source supplied them.
