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
    print("\nSetting servo motor IDs.")
    servo1 = LX16A(1)   # Front Ankle 
    servo2 = LX16A(2)   # Front Knee
    servo3 = LX16A(3)   # Left Ankle 
    servo4 = LX16A(4)   # Left Knee
    servo5 = LX16A(5)   # Back Ankle
    servo6 = LX16A(6)   # Back Knee
    servo7 = LX16A(7)   # Right Ankle 
    servo8 = LX16A(8)   # Right Knee
    print("Complete.\n")
except ServoArgumentError as e:
    print(f"Error setting servo IDs. The servo's ID is outside the range 0 - 253 degrees. Exiting...")
    quit()

# Run BOOT TEST
print("Running boot test for all servo motors.")
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
print("Complete.\n")

# Set servo angle limits
try:
    print("Setting angle limits for each servo motor.")
    servo1.set_angle_limits(0, 240)     # Front Ankle
    servo2.set_angle_limits(0, 127)     # Front Knee
    servo3.set_angle_limits(0, 240)     # Left Ankle
    servo4.set_angle_limits(0, 240)     # Left Knee
    servo5.set_angle_limits(0, 240)     # Back Ankle
    servo6.set_angle_limits(138, 240)   # Back Knee
    servo7.set_angle_limits(0, 240)     # Right Ankle
    servo8.set_angle_limits(0, 240)     # Right Knee 
    print("Complete.\n")
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
        print("Complete.\n")
    except ServoError as e:
        print(f"Error checking LED error triggers for servo {servo.get_id()}. Exiting...")
        quit()

# Homing proceedure - set motors to home position 
print("Setting servo motors to home position.")
try:
    servo1.move(147.36, 1000)   # setting servos to desired position and waiting 1000 milliseconds (=1sec)
    servo2.move(88.80, 1000)
    servo3.move(133.68, 1000)
    servo4.move(153.84, 1000)
    servo5.move(115.44, 1000)
    servo6.move(172.80, 1000)
    servo7.move(130.56, 1000)
    servo8.move(121.20, 1000)
    time.sleep(1.0)
    print("All servos are set and ready for movement.\n")
except ServoArgumentError as e:
    print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
except ServoLogicalError as e:
    print(f"The command is issued while in motor mode or while torque is disabled")

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
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion hello.wav")
    elif "minion" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion hello.wav")
    elif "hi" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion hello.wav")
    elif "greetings" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion hello.wav")
    elif "banana" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion banana.wav")
    elif "food" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion banana.wav")
    elif "hungry" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion banana.wav")
    elif "well done" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Ta da.wav")
    elif "good job" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Ta da.wav")
    elif "ta da" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Ta da.wav")
    elif "good work" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Ta da.wav")
    elif "bottom" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion bottom.wav")
    elif "ass" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion bottom.wav")
    elif "butt" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion bottom.wav")
    elif "fart" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion farting.wav")
    elif "smell" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion farting.wav")
    elif "rip" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion farting.wav")
    elif "funny" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion laughter.wav")
    elif "joke" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion laughter.wav")
    elif "laughing" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion laughter.wav")
    elif "haha" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion laughter.wav")
    elif "sing" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion singing.wav")
    elif "singing" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion singing.wav")
    elif "song" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion singing.wav")
    elif "music" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion singing.wav")
    elif "yay" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Yay.wav")
    elif "yes" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Yay.wav")
    elif "great" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Yay.wav")
    elif "Gru" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Yay.wav")
    elif "Despicable Me" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Yay.wav")
    elif "beedo" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion Noises 2.wav")
    elif "Kevin" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Kevin.wav")  # left off here 
    elif "why" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Why.wav")
    elif "argh" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Argh.wav")
    elif "fight" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Fight.wav")
    elif "angry" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Fight.wav")
    elif "toy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Pa poy.wav")
    elif "boss" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Mini boss.wav")
    elif "mini boss" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Mini boss.wav")
    elif "sad" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Cry.wav")
    elif "cry" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Cry.wav")
    elif "upset" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Cry.wav")
    elif "cow" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Moo.wav")
    elif "moo" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Moo.wav")
    elif "kung fu" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Kung Fu.wav")
    elif "smoochy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Kung Fu.wav")
    elif "annoying" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/No annoying sounds.wav")
    elif "hate" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Hate.wav")
    elif "guy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Hate.wav")
    elif "happy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Happy.wav")
    elif "fluffy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Fluffy.wav")
    elif "bob" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/King Bob.wav")
    elif "king" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/King Bob.wav")
    elif "what" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/What.wav")
    else:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/What.wav")
        print("Unknown command")

# Function to walk forward - using sin and cos waves (smooth motor motion as opposed to direcly calling angles --> triangle waves)
def forward_motion():
    print("\nBeginning forward motion.\n")
    try: 
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion whistle.wav")
    except ServoArgumentError as e:
        print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
    except ServoLogicalError as e:
        print(f"The command is issued while in motor mode or while torque is disabled")
        

# Function to begin backwards motion
def backward_motion():
    print("Begin backwards motion.\n")
    try:    
       play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion YMCA.wav")
    except ServoArgumentError as e:
        print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
    except ServoLogicalError as e:
        print(f"The command is issued while in motor mode or while torque is disabled")

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to listen for voice commands
def listen_for_commands():
    with sr.Microphone() as source:
        print("Listening for commands...\n")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Command recognized.\n")
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