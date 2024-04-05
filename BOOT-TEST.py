#!/usr/bin/env python3

from pylx16a.lx16a import *
import time

# Initializing the LX16A class
LX16A.initialize("/dev/cu.usbserial-110", 0.1)                  # initialize servo bus port                      

# Set servo IDs - should already be set from servo-test.py
try:
    servo1 = LX16A(1)
    servo2 = LX16A(2)
    servo3 = LX16A(3)
    servo4 = LX16A(4)
    servo5 = LX16A(5)
    servo6 = LX16A(6)
    servo7 = LX16A(7)
    servo8 = LX16A(8)
except ServoArgumentError as e:
    print(f"Error setting servo IDs. The servo's ID is outside the range 0 - 253 degrees. Exiting...")
    quit()

# Run BOOT TEST
try:
    servo1.set_vin_limits(5000, 11500)                           # sets voltage limits
    servo1.set_temp_limit(85)                                    # sets temp limit
    servo1.servo_mode()                                          # sets servos to servo mode
    servo1.enable_torque()                                       # enable torque
    servo1.led_power_on()                                        # powers on LED
    servo1.led_power_off()                                       # powers off LED
    servo1.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)    # sets LED error triggers
    servo2.set_vin_limits(5000, 11500)                           # sets voltage limits
    servo2.set_temp_limit(85)                                    # sets temp limit
    servo2.servo_mode()                                          # sets servos to servo mode
    servo2.enable_torque()                                       # enable torque
    servo2.led_power_on()                                        # powers on LED
    servo2.led_power_off()                                       # powers off LED
    servo2.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)    # sets LED error triggers
    servo3.set_vin_limits(5000, 11500)                           # sets voltage limits
    servo3.set_temp_limit(85)                                    # sets temp limit
    servo3.servo_mode()                                          # sets servos to servo mode
    servo3.enable_torque()                                       # enable torque
    servo3.led_power_on()                                        # powers on LED
    servo3.led_power_off()                                       # powers off LED
    servo3.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)    # sets LED error triggers
    servo4.set_vin_limits(5000, 11500)                           # sets voltage limits
    servo4.set_temp_limit(85)                                    # sets temp limit
    servo4.servo_mode()                                          # sets servos to servo mode
    servo4.enable_torque()                                       # enable torque
    servo4.led_power_on()                                        # powers on LED
    servo4.led_power_off()                                       # powers off LED
    servo4.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)    # sets LED error triggers
    servo5.set_vin_limits(5000, 11500)                           # sets voltage limits
    servo5.set_temp_limit(85)                                    # sets temp limit
    servo5.servo_mode()                                          # sets servos to servo mode
    servo5.enable_torque()                                       # enable torque
    servo5.led_power_on()                                        # powers on LED
    servo5.led_power_off()                                       # powers off LED
    servo5.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)    # sets LED error triggers
    servo6.set_vin_limits(5000, 11500)                           # sets voltage limits
    servo6.set_temp_limit(85)                                    # sets temp limit
    servo6.servo_mode()                                          # sets servos to servo mode
    servo6.enable_torque()                                       # enable torque
    servo6.led_power_on()                                        # powers on LED
    servo6.led_power_off()                                       # powers off LED
    servo6.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)    # sets LED error triggers
    servo7.set_vin_limits(5000, 11500)                           # sets voltage limits
    servo7.set_temp_limit(85)                                    # sets temp limit
    servo7.servo_mode()                                          # sets servos to servo mode
    servo7.enable_torque()                                       # enable torque
    servo7.led_power_on()                                        # powers on LED
    servo7.led_power_off()                                       # powers off LED
    servo7.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)    # sets LED error triggers
    servo8.set_vin_limits(5000, 11500)                           # sets voltage limits
    servo8.set_temp_limit(85)                                    # sets temp limit
    servo8.servo_mode()                                          # sets servos to servo mode
    servo8.enable_torque()                                       # enable torque
    servo8.led_power_on()                                        # powers on LED
    servo8.led_power_off()                                       # powers off LED
    servo8.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)    # sets LED error triggers
except ServoError as e:
    print(f"Error running the boot test. Servo {e.id_} is not responding. Exiting...")
    quit()

# Set servo angle limits
try:
    servo1.set_angle_limits(0, 240)
    servo2.set_angle_limits(0, 240)
    servo3.set_angle_limits(0, 240)
    servo4.set_angle_limits(0, 240)
    servo5.set_angle_limits(0, 240)
    servo6.set_angle_limits(0, 240)
    servo7.set_angle_limits(0, 240)
    servo8.set_angle_limits(0, 240)
except ServoArgumentError as e:
    print(f"Error setting servo angle limits. Servo {e.id_} is not responding. Either limit is out of the range or upper limit is less than lower. Exiting...")
    quit()

# Check LED error triggers and flash LED motor lights three times for each servo
servos = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8]
for servo in servos:
    try:
        over_temp, over_voltage, rotor_locked = servo.get_led_error_triggers()
        if not any([over_temp, over_voltage, rotor_locked]):
            # No error detected, flash LED lights three times
            for _ in range(3):
                servo.led_power_on()
                time.sleep(0.5)
                servo.led_power_off()
                time.sleep(0.5)
            print(f"Servo {servo.get_id()} is ready to go.")
    except ServoError as e:
        print(f"Error checking LED error triggers for servo {servo.get_id()}. Exiting...")
        quit()