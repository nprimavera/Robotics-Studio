#!/usr/bin/env python3

# Documentation from https://github.com/ethanlipson/PyLX-16A/blob/master/documentation.md python library LX16A

# Useful commands to know within the LX16A library


# Setter member functions 

LX16A.move          # rotate the servo
LX16A.move_start    # if a movement command has been set by LX16A.move(..., wait=True), then running this command will execute it
LX16A.move_stop     # halt servo movement

LX16A.set_bspline   # set the servo's B-spline curve
LX16A.move_bspline  # move to a point on a B-spline curve

LX16A.set_id        # gives the servo a new ID (changes the virtual servo's ID to match

LX16A.set_angle_offset  # set an angle offset applied to all move commands

LX16A.set_angle_limits  # set angle limits to servo rotation
LX16A.set_vin_limits    # set input voltage limits
LX16A.set_temp_limit    # set temperature limits in degrees Celsius

LX16A.motor_mode        # switch the servo to motor mode and set its rotation speed --> will not need this for robot
LX16A.servo_mode        # switch the servo to servo mode

LX16A.enable_torque     # allow the servo to produce torque and prevent it from easily giving to external forces
LX16A.disable_torque    # prevent the servo from producing torque and allow it to easily give to external forces

LX16A.led_power_on      # light up the servo's LED
LX16A.led_power_off     # shut off the servo's LED
LX16A.set_led_error_triggers    # set what conditions cause the servo's LED to flash


# Getter member functions

LX16A.get_last_instant_move_hw  # Get the angle and time of the last call to LX16A.move(..., wait=False)
LX16A.get_last_delayed_move_hw  # Get the angle and time of the last call to LX16A.move(..., wait=True)

LX16A.get_id    # Get the ID of the servo (to avoid making a physical query, servo.id_ can be used instead)

LX16A.get_angle_offset  # Get the servo's angle offset
LX16A.get_angle_limits  # Get the servo's angle limits

LX16A.get_vin_limits # Get the servo's input voltage limits

LX16A.get_temp_limit # Get the servo's temperature limit in degrees Celsius

LX16A.is_motor_mode   # Check if the servo is in motor mode
LX16A.get_motor_speed # If the servo is in motor mode, get its speed

LX16A.is_torque_enabled # Check if the servo is allowed to produce torque

LX16A.is_led_power_on        # Check if the servo's LED is currently enabled
LX16A.get_led_error_triggers # Check what conditions will cause the servo's LED to flash

LX16A.get_temp # Get the servo's current temperature

LX16A.get_vin # Get the servo's current input voltage

LX16A.get_physical_angle # Get the servo's physical angle
LX16A.get_commanded_angle # Get the servo's commanded angle
LX16A.get_waiting_angle # Get the servo's waiting angle, if set by LX16A.move(..., wait=True)


# Using the commands

from math import sin, cos
from pylx16a.lx16a import *
import time


# Initializing the LX16A class 
@staticmethod LX16A.initialize(port: str, timeout: float = 0.02) -> None   # initializes the LX16A class with the servo bus controller's port 
LX16A.initialize("/dev/cu.usbserial-110", 0.1)   # what I use for my MAC


# Using LX16A.__init__  -   the __init__ method is used for initializing newly created objects and it is automatically called when you create a new instance of class 
try:
    LX16A.__init__(self, id: int, disable_torque: bool = False) -> None  # servo object constructor - if true the servo initializes with torque disabled 
except ServoArgumentError as e:
    print(f"Servo {e.id_} is outside the range 0 - 253. Exiting...")


# Correct way to utilize exceptions 
try:

except ServoError as e:   # ServoTimeoutError, ServoChecksumError, ServoArgumentError, and ServoLogicalError all inherit from ServoError, which will catch them all 
    print(f"Servo {e.id_} is not responding. Exiting...")   # All servo exceptions have an "id_" member variable containing the errant servo's ID 
    quit()


# Timeouts
@staticmethod set_timeout(seconds: float) -> None   # set the serial port's read and write timeouts
@staticmethod get_timeout() -> float                # get the serial port's read and write timeout


# Move
try:
    LX16A.move(angle: float, time: float = 0, relative: bool = False, wait: bool = False) -> None   # move servo to specified angle with options to control rotation duration, relativity, and delay
except ServoArgumentError as e:
    print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
except ServoLogicalError as e:
    print(f"The command is issued while in motor mode or while torque is disabled")
# Can use ServoError to catch both


# Move start
try:
    LX16A.move_start() -> None  # if a movement command has been set by LX16A.move(..., wait=True), running this command will execute it
except ServoLogicalError as e:
    print(f"Either no move command has been set by LX16A.move(...,wait=True), the command is issued while in motor mode, or the command is issued while torque is disabled")


# Move stop
try:
    LX16A.move_stop() -> None   # halts the servo's movement
except ServoLogicalError as e:
    print(f"The command is issued while in motor mode")


# Get last instant move
try:
    LX16A.get_last_instant_move_hw() -> tuple[float, int]   # gets the angle and time parameters from the most recent call to LX16A.move(..., wait=False)
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Get last delayed move
try:
    LX16A.get_last_delayed_move_hw() -> tuple[float, int]   # gets the angle and time parameters from the most recent call to LX16A.move(..., wait=True)
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Set B-spline
try:
    set_bspline(knots: list[float], control_points: list[tuple[float, float]], degree: int, num_samples: int = 100) -> None # set the servo's B-spline to be used by LX16A.move_bspline
except ServoArgumentError as e:
    print(f"len(knots) != len(control_points) - degree + 1")


# Move B-spline
try:
    LX16A.move_bspline(x: float, time: int = 0, wait: bool = False) -> None  # samples a point on the B-spline curve set by LX16A.set_bspline and moves to it
except ServoLogicalError as e:
    print(f"No B-spline has been set by LX16A.set_bspline")


# Set motor id - already did this using servo-test.py 
try:
    LX16A.set_id(id: int) -> None   # gives the servo a new ID - the class instance's internal ID is updated as well
except ServoArgumentError as e:
    print(f"The servo's ID is outside the range 0 - 253")


# Get servo ID
try:
    LX16A.get_id(poll_hardware: bool = False) -> int    # gets the servo's ID set by LX16A.set_id
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Set angle offsets
try:
    LX16A.set_angle_offset(offset: int, permanent: bool = False) -> None    # creates an offset for move commands - all angle readings will automatically correct for the offset
except ServoArgumentError as e:
    print(f"The offset is outside the range -30 degrees to 30 degrees")


# Get angle offsets
try:
    LX16A.get_angle_offset(poll_hardware: bool = False) -> int  # gets the servo's angle offset
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Set angle limits
try:
    LX16A.set_angle_limits(lower_limit: float, upper_limit: float) -> None  # creates lower and upper angle limits for move commands
except ServoArgumentError as e:
    print(f"Either limit is out of the range 0 - 240 degrees or the upper limit is less than the lower limit")


# Get angle limits
try:
    LX16A.get_angle_limits(poll_hardware: bool = False) -> tuple[float, float]  # gets the servo's angle limits
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Get the servo's physical angle
try:
    LX16A.get_physical_angle() -> float     # gets the physical angle of the servo - note: this angle may not be equal to the command angle LX16A.get_command_angle, such as in the case of excessive load
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Get the command angle
LX16A.get_command_angle() -> float      # gets the command angle of the servo


# Get waiting angle
try:
    LX16A.get_waiting_angle() -> float  # gets the servo's waiting angle, if set by LX16A.move(..., wait=True)
except ServoLogicalError as e:
    print(f"No move has been set by LX16A.move(..., wait=True)")


# Set voltage limits
try:
    LX16A.set_vin_limits(lower_limit: int, upper_limit: int) -> None    # creates lower and upper voltage limits for the servo
    # if these limits have been violated and the voltage condition has been enabled using set_led_error_triggers, the servo's LED will flash
except ServoArgumentError as e:
    print(f"Either limit is outside the range of 4500 - 12000 millivolts or the upper limit is less than the lower limit")


# Get voltage limits
try:
    LX16A.get_vin_limits(poll_hardware: bool = False) -> tuple[int, int]    # gets the servo's input voltage limits
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Get the input voltage of the servo
try:
    LX16A.get_vin() -> int  # gets the input voltage of the servo in millivolts
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Set temperature limits
try:
    LX16A.set_temp_limit(upper_limit: int) -> None  # creates an upper temperature limit for the servo - should be set to 85 degrees celcius 
    # if the limit is violated and the temperature condition has been enabled using set_led_error_triggers, the servo's LED will flash
except ServoArgumentError as e:
    print(f"The limit is outside the range 50 degrees celcius to 100 degrees celcius")


# Get temp limits
try:
    LX16A.get_temp_limit(poll_hardware: bool = False) -> None   # gets the servo's temperature limit
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Get servo temperature
try:
    LX16A.get_temp() -> int     # gets the temperature of the servo in degrees celcius
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Set servos to motor mode
try:
    LX16A.motor_mode(speed: int) -> None    # switches the servo to motor mode, where the rotation speed is controlled instead of the angle
except ServoArgumentError as e:
    print(f"The motor speed is outside the range -1000 to 1000")
except ServoLogicalError as e:
    print(f"Torque is disabled")


# Check if the servo is in motor mode
try:
    LX16A.is_motor_mode(poll_hardware: bool = False) -> bool    # checks if the servo is in motor mode
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Get motor speed
try:
    LX16A.get_motor_speed(poll_hardware: bool = False) -> int   # if the servo is in motor mode, gets its speed 
except ServoLogicalError as e:
    print(f"The servo is not in motor mode")
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Set servos to servo mode - should already be done using servo-test.py
LX16A.servo_mode() -> None


# Enable torque 
try:
    LX16A.enable_torque() -> None   # allows the servo to produce torque and stops it from being rotated manually
except ServoLogicalError as e:
    print(f"Torque is already enabled")


# Check if torque is enabled
try:
    LX16A.is_torque_enabled(poll_hardware: bool = False) -> bool    # check if the servo can produce torque
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# Disable torque
try:
    LX16A.disable_torque() -> None  # prevents the servo from producing torque and lets it be rotated manually
except ServoLogicalError as e:
    print(f"Torque is already disabled")


# LED power on
LX16A.led_power_on() -> None    # powers on the servo's LED - even if this function is not called, the LED will still flash if any of the error conditions set by LX16A.set_led_error_triggers are met


# Check if LED power is on
try:
    LX16A.is_led_power_on(poll_hardware: bool = False) -> bool  # checks if the servo's LED is powered on
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")


# LED power off
LX16A.led_power_off() -> None    # powers off the servo's LED -  even if this function is not called, the LED will still flash if any of the error conditions set by LX16A.set_led_error_triggers are met


# Set LED error triggers 
LX16A.set_led_error_triggers(over_temperature: bool, over_voltage: bool, rotor_locked: bool) -> None    # sets what error conditions will cause the servo's LED to flash


# Get LED triggers
try:
    LX16A.get_led_error_triggers(poll_hardware: bool = False) -> tuple[bool, bool, bool]    # checks what error conditions will cause the servo's LED to flash
except ServoTimeoutError as e:
    print(f"The program received less bytes than expected")
except ServoChecksumError as e:
    print(f"The program received a bad checksum")





















