# 🛠️ Guide: Adding a Termination Resistor in an RJ45 Plug (Modbus RTU)

## ✅ Background

A properly placed 120-ohm termination resistor is essential for stable Modbus RS-485 communication.
In your setup — X1 Mini inverter, RJ45 direct connection, and Modbus via USB stick at 9600 baud over approx. 15 m cable — the termination resistor is particularly important, especially when there are no other devices on the bus.

## 🎯 Goal

Install a 120-ohm resistor between Pin 4 (Modbus A/+) and Pin 5 (Modbus B/–) inside an RJ45 plug — using as little space as possible so the IP65 cover still closes.

## 🧰 You will need

- 1x RJ45 plug (8P8C, shielded or unshielded depending on cable)
- 1x 120-ohm resistor (ideally ¼ W, axial)
- 2x 470-ohm resistors for optional pull-up/pull-down (see 💡 Tips)
- 1x Ethernet cable (e.g. patch cable)
- Crimping tool for RJ45
- Wire cutters / stripper
- Heat shrink tubing (optional)
- Multimeter (optional for checking)

## 🔌 Modbus over RJ45 Pinout

| Pin | Signal       | Function         |
|-----|--------------|------------------|
| 4   | Modbus A / D+ | Data line +      |
| 5   | Modbus B / D– | Data line –      |

## 🧱 Step-by-Step Instructions

### 1. Prepare the resistor

- Trim the resistor leads to ~1 cm.
- Bend the ends slightly so they can be inserted into Pin 4 and Pin 5.

### 2. Prepare the cable

- Strip 2–3 cm of the outer jacket of the RJ45 cable.
- Strip about 5 mm of insulation from the wires for Pin 4 (blue) and Pin 5 (blue-white).

### 3. Insert the resistor

- Solder or crimp the resistor directly between wires for Pin 4 and 5, or
- Insert the resistor legs directly into the respective channels of the RJ45 plug.

### 4. Add heat shrink tubing (optional)

- Insulate the resistor with heat shrink or tape to prevent shorting other pins.

### 5. Crimp the RJ45 plug

- Ensure the wires are positioned correctly and the resistor sits snugly but not pinched.
- Insert into crimp tool (8P port) and crimp firmly.

## 📏 Optional Check

- Use a multimeter in resistance mode.
- Measure between Pin 4 and Pin 5 → should read ~120 Ω if everything is correct.

## 📦 Usage

- Plug the RJ45 into the inverter’s Modbus port (e.g. X1 Mini).
- The IP65 cover should close without pressure.
- Restart Modbus and check logs or status.

## 💡 Tips

- In RS-485 networks, **exactly two termination resistors** should be used — one at each end of the bus.

- For additional stability, especially with long cables or unreliable devices, you may add:
  - A **470 Ω pull-up resistor** between A (Pin 4) and **3.3 V**
  - A **470 Ω pull-down resistor** between B (Pin 5) and **GND**

These resistors help improve line biasing and prevent noise when the bus is idle.