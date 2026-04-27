import time
from piper_sdk import *

# CONFIG 
CAN_PORT = "can0"
SPEED    = 30      # percent (0–100)
SETTLE   = 2.0     # seconds to wait after each move

# Point A: [x_m, y_m, z_m, roll_deg, pitch_deg, wrist_yaw_deg]
POINT_A = [0.25, 0.00, 0.30, 0.0, 90.0, 0.0]

# Point B: same XYZ, wrist rotated 45°
POINT_B = [0.35, 0.05, 0.20, 0.0, 90.0, 45.0]

def connect(can_port):
    piper = C_PiperInterface(can_name=can_port, can_auto_init=True, dh_is_offset=1)
    piper.ConnectPort()
    piper.EnableArm(7)
    time.sleep(0.5)
    piper.MotionCtrl_2(0x01, 0x01, SPEED)  # CAN ctrl, Cartesian mode
    return piper

def move(piper, x_m, y_m, z_m, roll_deg, pitch_deg, wrist_yaw_deg):
    """
    XYZ in metres, angles in degrees.
    SDK internal units: 0.001 mm for XYZ = multiply by 1e6
                        0.001 deg for angles = multiply by 1000
    wrist_yaw_deg (RZ) is the terminal wrist rotation.
    """
    piper.EndPoseCtrl(
        int(x_m        * 1e6),
        int(y_m        * 1e6),
        int(z_m        * 1e6),
        int(roll_deg   * 1000),
        int(pitch_deg  * 1000),
        int(wrist_yaw_deg * 1000),   # wrist angle
    )

if __name__ == "__main__":
    piper = connect(CAN_PORT)

    print("Moving to Point A...")
    move(piper, *POINT_A)
    time.sleep(SETTLE)

    print("Moving to Point B (wrist rotate + arm translation)...")
    move(piper, *POINT_B)
    time.sleep(SETTLE)

    print("Done.")