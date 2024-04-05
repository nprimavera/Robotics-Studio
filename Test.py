#!/usr/bin/env python3
# Version 1.1.2

# Will not need all of these but imported just in case 
from math import sin, cos
from pylx16a.lx16a import *
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QComboBox,
    QListWidget,
    QLabel,
    QSlider,
    QLineEdit,
    QRadioButton,
    QCheckBox,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIntValidator
import serial.tools.list_ports
import serial.serialutil
import platform
import sys
import time

# Initializing the LX16A class
LX16A.initialize("/dev/cu.usbserial-110", 0.1)

# Run BOOT TEST

# Set voltage limits
try:
    LX16A.set_vin_limits(lower_limit=4500, upper_limit=12000)    # creates lower and upper voltage limits for the servo
    # if these limits have been violated and the voltage condition has been enabled using set_led_error_triggers, the servo's LED will flash
except ServoArgumentError as e:
    print(f"Either limit is outside the range of 4500 - 12000 millivolts or the upper limit is less than the lower limit")

# Set temperature limits
try:
    LX16A.set_temp_limit(upper_limit=85)   # creates an upper temperature limit for the servo - should be set to 85 degrees celcius 
    # if the limit is violated and the temperature condition has been enabled using set_led_error_triggers, the servo's LED will flash
except ServoArgumentError as e:
    print(f"The limit is outside the range 50 degrees celcius to 100 degrees celcius")

# Set servos to servo mode - should already be done using servo-test.py
LX16A.servo_mode() 

# Enable torque 
try:
    LX16A.enable_torque()   # allows the servo to produce torque and stops it from being rotated manually
except ServoLogicalError as e:
    print(f"Torque is already enabled")

# Set motor id - already did this using servo-test.py 
#try:
    #LX16A.set_id(id: int) -> None   # gives the servo a new ID - the class instance's internal ID is updated as well
#except ServoArgumentError as e:
    #print(f"The servo's ID is outside the range 0 - 253")

# Set angle limits
try:
    LX16A.set_angle_limits(lower_limit=0, upper_limit=240)  # creates lower and upper angle limits for move commands
except ServoArgumentError as e:
    print(f"Either limit is out of the range 0 - 240 degrees or the upper limit is less than the lower limit")

# LED power on
LX16A.led_power_on()    # powers on the servo's LED - even if this function is not called, the LED will still flash if any of the error conditions set by LX16A.set_led_error_triggers are met

# LED power off
LX16A.led_power_off()   # powers off the servo's LED -  even if this function is not called, the LED will still flash if any of the error conditions set by LX16A.set_led_error_triggers are met

# Set LED error triggers 
LX16A.set_led_error_triggers(over_temperature=False, over_voltage=False, rotor_locked=False)    # sets what error conditions will cause the servo's LED to flash

# Flash LEDs if everything is ready to go 
LX16A.led_power_on()    # powers on the servo's LED - even if this function is not called, the LED will still flash if any of the error conditions set by LX16A.set_led_error_triggers are met

# Check if error triggers are not activated
if not LX16A.is_led_error_on():
    # Flash the LEDs of all servos three times
    for servo_id in range(1, 9):  # servo IDs from 1 to 8
        # Turn on the LED
        LX16A(id=servo_id).led_power_on()
        # Wait for half a second
        time.sleep(0.5)
        # Turn off the LED
        LX16A(id=servo_id).led_power_off()
        # Wait for half a second
        time.sleep(0.5)
        # Repeat the flashing two more times


# Walking

