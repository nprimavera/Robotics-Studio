#!/usr/bin/env python3

import math
from lx16a import *
import time
from math import sin, cos

# Initializing the LX16A class
#LX16A.initialize("/dev/cu.usbserial-110", 0.1)                   # initialize servo bus port - for MAC 
#LX16A.initialize(COM3)                                           #   "    "    "   - for Windows 
LX16A.initialize("/dev/ttyUSB0", 0.1)                             #   "    "    "   - for Raspberry Pi     

# Set servo IDs
try:
    print("\nSetting servo IDs.")
    servo1 = LX16A(1)   # Front Ankle 
    servo2 = LX16A(2)   # Front Knee
    servo3 = LX16A(3)   # Left Ankle 
    servo4 = LX16A(4)   # Left Knee
    servo5 = LX16A(5)   # Back Ankle
    servo6 = LX16A(6)   # Back Knee
    servo7 = LX16A(7)   # Right Ankle 
    servo8 = LX16A(8)   # Right Knee
    print("Servo IDs complete.\n")
except ServoArgumentError as e:
    print(f"Error setting servo IDs. The servo's ID is outside the range 0 - 253 degrees. Exiting...")
    quit()

# Run BOOT TEST
print("Running boot test for all servos.")
servos = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8]
for servo in servos:
    try:
        servo.set_vin_limits(5000, 11500)
        servo.set_temp_limit(85)
        servo.servo_mode()
        servo.enable_torque()
        servo.led_power_on()
        servo.led_power_off()
        servo.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)
        print(f"Boot test for servo {servo.get_id()} is complete.")
        time.sleep(0.3)
    except ServoError as e:
        print(f"Error running the boot test. Servo {e.id_} is not responding. Exiting...")
        quit()
print("Boot test complete.\n")

# Set servo angle limits
try:
    print("Setting angle limits for each servo.")
    servo1.set_angle_limits(0, 240)     # Front Ankle
    servo2.set_angle_limits(81, 240)    # Front Knee
    servo3.set_angle_limits(0, 240)     # Left Ankle
    servo4.set_angle_limits(0, 240)     # Left Knee
    servo5.set_angle_limits(0, 240)     # Back Ankle
    servo6.set_angle_limits(138, 240)   # Back Knee
    servo7.set_angle_limits(0, 240)     # Right Ankle
    servo8.set_angle_limits(0, 240)     # Right Knee 
    print("Angle limits complete.\n")
except ServoArgumentError as e:
    print(f"Error setting servo angle limits. Servo {e.id_} is not responding. Either limit is out of the range or upper limit is less than lower. Exiting...")
    quit()

# Health check - check LED error triggers and flash LED motor lights three times for each servo
print("Beginning servo health check.")
servos = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8]
for servo in servos:
    try:
        over_temp, over_voltage, rotor_locked = servo.get_led_error_triggers()
        if not any([over_temp, over_voltage, rotor_locked]):
            # No error detected, flash LED lights three times
            for _ in range(3):
                servo.led_power_on()
                time.sleep(0.1)
                servo.led_power_off()
                time.sleep(0.1)
            print(f"Servo {servo.get_id()} is ready.")
    except ServoError as e:
        print(f"Error checking LED error triggers for servo {servo.get_id()}. Exiting...")
        quit()

# Homing proceedure - set angles to home position 
print("\nSetting servos to home position.")
try:
    servo1.move(145.68, 1000)   # setting servos to desired position and waiting 1000 milliseconds 
    servo2.move(115.92, 1000)
    servo3.move(141.84, 1000)
    servo4.move(155.52, 1000)
    servo5.move(114.52, 1000)
    servo6.move(172.08, 1000)
    servo7.move(130.56, 1000)
    servo8.move(122.16, 1000)
    time.sleep(1.0)
except ServoArgumentError as e:
    print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
except ServoLogicalError as e:
    print(f"The command is issued while in motor mode or while torque is disabled")
print("All servos are set and ready for movement.\n")

# Print initial angles
print("Initial angle positions:")
try:
    for servo in servos:
        servo.get_physical_angle()     # gets the physical angle of the servo - note: this angle may not be equal to the command angle LX16A.get_command_angle, such as in the case of excessive load
        print(f"Servo {servo.get_id()} is at {servo.get_physical_angle()}.")
        time.sleep(0.3)
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")

# Testing leg movement 
try:
    # Move front and back legs 
    servo1.move(165.68, 100)
    time.sleep(0.25)
    servo1.move(125.79, 100)
    time.sleep(0.25)
    servo1.move(145.68)
    #servo2.move()
    #servo5.move()
    #servo6.move()
    time.sleep(0.25)
    # Move left and right legs 
    #servo3.move()
    #servo4.move()
    #servo7.move()
    #servo8.move()
    time.sleep(0.25)
except ServoArgumentError as e:
    print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
except ServoLogicalError as e:
    print(f"The command is issued while in motor mode or while torque is disabled")