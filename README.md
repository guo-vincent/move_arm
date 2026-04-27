# move_arm

A minimal Python script for moving an [AgileX Piper](https://global.agilex.ai/products/piper) robotic arm from one Cartesian pose to another with explicit wrist angle control. Uses only `piper_sdk` and the Python standard library.

---

## What it does

`move_arm.py` connects to the Piper over CAN, enables the arm, and commands it to move sequentially through two end-effector poses (Point A to Point B). Each pose is defined as a full 6-DOF Cartesian target: position in XYZ (metres) plus orientation as roll/pitch/wrist-yaw (degrees). The wrist angle — the rotation of the terminal joint about the tool's own Z-axis — is the primary parameter this script is designed to vary.

---

## Requirements

### Hardware

- AgileX Piper arm
- USB-to-CAN adapter connected to the arm

### Software

- Linux (Ubuntu 18.04 / 20.04 / 22.04)
- Python 3.6+
- `piper_sdk`

###

```bash
pip install piper-sdk
```

---

## CAN bus setup

The CAN interface must be active before running the script.

```bash
sudo ip link set can0 type can bitrate 1000000
sudo ip link set can0 up
```

Verify with:

```bash
ip link show can0
```

You should see `UP` in the flags. If your adapter appears under a different name (e.g. `can_piper`), update the `CAN_PORT` variable in the script accordingly.

---

## Usage

```bash
python move_arm.py
```

Edit the constants at the top of the script to change the target poses:

```python
# Point A: [x_m, y_m, z_m, roll_deg, pitch_deg, wrist_yaw_deg]
POINT_A = [0.25, 0.00, 0.30, 0.0, 90.0, 0.0]

# Point B: same position, wrist rotated 45°
POINT_B = [0.25, 0.00, 0.30, 0.0, 90.0, 45.0]
```

`SPEED` (0–100) controls the motion speed as a percentage of the arm's maximum.  
`SETTLE` is the number of seconds the script waits after issuing each move command before proceeding.

---

## How wrist angle control works

The Piper SDK's `EndPoseCtrl` function accepts a full Cartesian pose as six integers scaled to internal units:

| Parameter | Meaning | Scale factor |
|---|---|---|
| `X, Y, Z` | End-effector position | metres × 1,000,000 |
| `RX, RY` | Roll and pitch of the tool | degrees × 1,000 |
| `RZ` | **Wrist yaw — the wrist angle** | degrees × 1,000 |

`RZ` rotates the end-effector around its own Z-axis without changing its XYZ position or the roll/pitch orientation. This is the parameter to vary when you want the arm to approach the same point with the hand at a different angle — for example, picking up a tool at 0°, 45°, or 90°.

---

## Important notes

**Singularities.** `EndPoseCtrl` moves the arm in a straight Cartesian line. If the straight-line path between two poses passes through a kinematic singularity, the firmware will silently refuse the command. If this happens, break the motion into intermediate waypoints, or switch the script to joint-space mode (`MotionCtrl_2(0x01, 0x00, SPEED)` with `JointCtrl`).

**Firmware version.** The script uses `dh_is_offset=1`, which selects the DH parameter set for firmware `S-V1.6-3` and later. For older firmware, set `dh_is_offset=0`.

**Enable delay.** A 0.5-second sleep after `EnableArm` is required to give the firmware time to confirm the enable state before motion commands are sent. Removing it can cause the first command to be silently dropped.

---

## File structure

```markdown
move_arm/
└── move_arm.py   # main script
```
