#!/usr/bin/env python3

import math
import time
import speech_recognition as sr
import pygame

from lx16a import *
from math import sin, cos, pi

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

# Initialize pygame for audio output
pygame.mixer.init()

# Functions to play audio files
def play_audio(file_name):             # audio files need to be in the same directory as the python script 
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()

# Function to process voice commands
def process_command(command):
    if "forward" in command:
        forward_motion()
    elif "walk" in command:
        forward_motion()
    elif "step" in command:
        forward_motion()
    elif "backward" in command:
        backward_motion()
    elif "hello" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion hello.m4a")
    elif "hi" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion hello.m4a")
    elif "greetings" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion hello.m4a")
    elif "banana" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion banana.m4a")
    elif "food" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion banana.m4a")
    elif "hungry" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion banana.m4a")
    elif "minion" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Ta da.m4a")
    elif "bottom" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion bottom.m4a")
    elif "ass" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion bottom.m4a")
    elif "butt" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion bottom.m4a")
    elif "fart" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion farting.m4a")
    elif "smell" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion farting.m4a")
    elif "funny" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion laughter.m4a")
    elif "joke" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion laughter.m4a")
    elif "laughing" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion laughter.m4a")
    elif "sing" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion singing.m4a")
    elif "song" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion singing.m4a")
    elif "music" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion singing.m4a")
    elif "yay" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Yay.m4a")
    elif "yes" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Yay.m4a")
    elif "great" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Yay.m4a")
    elif "Gru" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Yay.m4a")
    elif "beedo" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Noises 2.m4a")
    else:
        print("Unknown command")

# Function to walk forward - using sin and cos waves (smooth motor motion)
def forward_motion():
    print("\nBeginning forward motion.\n")
    try: 
        # Start motion
        start_time = time.time()    # sets the start time = current timestamp 
        duration = 5.0              # run the motion for 5 seconds

        while time.time() - start_time < duration:      # while the current time stamp - start time is less than 5 seconds, run the code
            current_time = time.time() - start_time     # current time = time stamp - start time 
            play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion whistle.m4a")

            # Move front and back legs
            servo1_angle = 145.68 + (20 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo1.move(servo1_angle, 100)
            print(f"Servo 1 is at {servo1_angle} degrees.\n")
            servo2_angle = 115.92 + (15 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo2.move(servo2_angle, 100)
            print(f"Servo 2 is at {servo2_angle} degrees.\n")
            servo5_angle = 114.52 + (20 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo5.move(servo5_angle, 100)
            print(f"Servo 5 is at {servo5_angle} degrees.\n")
            servo6_angle = 172.08 - (15 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo6.move(servo6_angle, 100)
            print(f"Servo 6 is at {servo6_angle} degrees.\n")
            time.sleep(0.1)

            # Move left and right legs 
            servo3_angle = 141.84 + (20 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo3.move(servo3_angle, 100)
            print(f"Servo 3 is at {servo3_angle} degrees.\n")
            servo4_angle = 155.52 + (15 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo4.move(servo4_angle, 100)
            print(f"Servo 4 is at {servo4_angle} degrees.\n")
            servo7_angle = 130.56 - (20 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo7.move(servo7_angle, 100)
            print(f"Servo 7 is at {servo7_angle} degrees.\n")
            servo8_angle = 122.16 - (15 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo8.move(servo8_angle, 100)
            print(f"Servo 8 is at {servo8_angle} degrees.\n")
            time.sleep(0.1)                
    except ServoArgumentError as e:
        print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
    except ServoLogicalError as e:
        print(f"The command is issued while in motor mode or while torque is disabled")

    # Set servos back home 
    try:
        servo1.move(145.68, 100)   
        servo2.move(115.92, 100)
        servo3.move(141.84, 100)
        servo4.move(155.52, 100)
        servo5.move(114.52, 100)
        servo6.move(172.08, 100)
        servo7.move(130.56, 100)
        servo8.move(122.16, 100)
        time.sleep(1.0)
    except ServoArgumentError as e:
        print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
    except ServoLogicalError as e:
        print(f"The command is issued while in motor mode or while torque is disabled")
    print("Forward motion complete.\n")
    time.sleep(1.0)

# Function to begin backwards motion
def backward_motion():
    print("Begin backwards motion.\n")
    try: 
        # Start motion
        start_time = time.time()    # sets the start time = current timestamp 
        duration = 5.0              # run the motion for 5 seconds

        while time.time() - start_time < duration:      # while the current time stamp - start time is less than 5 seconds, run the code
            current_time = time.time() - start_time     # current time = time stamp - start time 
            play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion YMCA.m4a")

            # Move front and back legs
            servo1_angle = 145.68 - (20 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo1.move(servo1_angle, 100)
            print(f"Servo 1 is at {servo1_angle} degrees.\n")
            servo2_angle = 115.92 - (15 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo2.move(servo2_angle, 100)
            print(f"Servo 2 is at {servo2_angle} degrees.\n")
            servo5_angle = 114.52 - (20 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo5.move(servo5_angle, 100)
            print(f"Servo 5 is at {servo5_angle} degrees.\n")
            servo6_angle = 172.08 + (15 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo6.move(servo6_angle, 100)
            print(f"Servo 6 is at {servo6_angle} degrees.\n")
            time.sleep(0.1)

            # Move left and right legs 
            servo3_angle = 141.84 - (20 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo3.move(servo3_angle, 100)
            print(f"Servo 3 is at {servo3_angle} degrees.\n")
            servo4_angle = 155.52 - (15 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo4.move(servo4_angle, 100)
            print(f"Servo 4 is at {servo4_angle} degrees.\n")
            servo7_angle = 130.56 + (20 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo7.move(servo7_angle, 100)
            print(f"Servo 7 is at {servo7_angle} degrees.\n")
            servo8_angle = 122.16 + (15 * math.sin((2 * math.pi / 1) * current_time + 0))
            servo8.move(servo8_angle, 100)
            print(f"Servo 8 is at {servo8_angle} degrees.\n")
            time.sleep(0.1)                
    except ServoArgumentError as e:
        print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
    except ServoLogicalError as e:
        print(f"The command is issued while in motor mode or while torque is disabled")

    # Set servos back home 
    try:
        servo1.move(145.68, 100)   
        servo2.move(115.92, 100)
        servo3.move(141.84, 100)
        servo4.move(155.52, 100)
        servo5.move(114.52, 100)
        servo6.move(172.08, 100)
        servo7.move(130.56, 100)
        servo8.move(122.16, 100)
        time.sleep(1.0)
    except ServoArgumentError as e:
        print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
    except ServoLogicalError as e:
        print(f"The command is issued while in motor mode or while torque is disabled")
    print("Backward motion complete.\n")
    time.sleep(1.0)

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to listen for voice commands
def listen_for_commands():
    with sr.Microphone() as source:
        print("Listening for commands...\n")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing command...\n")
        command = recognizer.recognize_google(audio)
        print("Command:", command)
        process_command(command)
    except sr.UnknownValueError:
        print("\nCould not understand audio")
    except sr.RequestError as e:
        print("\nCould not request results; {0}".format(e))

# Main loop
while True:
    listen_for_commands()