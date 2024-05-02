#!/usr/bin/env python3

import math
import time
import speech_recognition as sr
import pygame
import pyaudio

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
    except ServoError as e:
        print(f"Error checking LED error triggers for servo {servo.get_id()}. Exiting...")
        quit()
print("Complete.\n")

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
    elif "how are you" in command:
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
    elif "Dave" in command:
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
    elif "uhh" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Argh.wav")
    elif "fight" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Fight.wav")
    elif "angry" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Fight.wav")
    elif "toy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Pa poy.wav")
    elif "Pa poy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Pa poy.wav")
    elif "boss" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Mini boss.wav")
    elif "Nico" in command:
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
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Smoochy smoochy.wav")
    elif "annoying" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/No annoying sounds.wav")
    elif "hate" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Hate.wav")
    elif "guy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Hate.wav")
    elif "savvas" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Hate.wav")
    elif "max" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Hate.wav")
    elif "adrian" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Hate.wav")
    elif "kuch" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Hate.wav")
    elif "happy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Happy.wav")
    elif "excited" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Happy.wav")
    elif "fluffy" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Fluffy.wav")
    elif "stuffed animal" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Fluffy.wav")
    elif "bob" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/King Bob.wav")
    elif "king" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/King Bob.wav")
    elif "what" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/What.wav")
    elif "confused" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/What.wav")
    elif "what are you doing" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/What.wav")
    elif "whistle" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion whistle.wav")
    elif "YMCA" in command:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion YMCA.wav")
    else:
        play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/What.wav")
        print("Unknown command")

# Function to walk forward - using sin and cos waves (smooth motor motion as opposed to direcly calling angles --> triangle waves)
def forward_motion():
    print("\nBeginning forward motion.\n")
    try: 
        for _ in range(3):
            play_audio("/home/nprimavera/Desktop/PyLX-16A-master/Minion noises/Minion whistle.wav")

            # Move front and back legs from start to point 1 - knee moving to max, ankle moving to min
            servo1_angle1_time = 0.10880398750305176
            servo1_angle1 = 147.36 + (20 * math.sin((2 * math.pi / 1) * servo1_angle1_time + math.pi))
            servo1.move(servo1_angle1, 100)
            print(f"Servo 1 is at {servo1_angle1} degrees. Moving to min.")
            servo2_angle1_time = 0.10965418815612793
            servo2_angle1 = 88.80 + (20 * math.sin((2 * math.pi / 1) * servo2_angle1_time + math.pi))
            servo2.move(servo2_angle1, 100)
            print(f"Servo 2 is at {servo2_angle1} degrees. Moving to max.")
            servo5_angle1_time = 0.10376381874084473
            servo5_angle1 = 115.44 + (20 * math.sin((2 * math.pi / 1) * servo5_angle1_time + math.pi))
            servo5.move(servo5_angle1, 100)
            print(f"Servo 5 is at {servo5_angle1} degrees. Moving to min.")
            servo6_angle1_time = 0.10975313186645508
            servo6_angle1 = 172.80 + (20 * math.sin((2 * math.pi / 1) * servo6_angle1_time + math.pi))
            servo6.move(servo6_angle1, 100)
            print(f"Servo 6 is at {servo6_angle1} degrees. Moving to max.\n")
            time.sleep(0.2)

            print("Front and back legs from start to point 1.\n")

            # Move front and back legs from point 1 to point 2 - knee at max, ankle at min 
            servo1_angle2_time = 0.27066493034362793
            servo1_angle2 = 147.36 + (20 * math.sin((2 * math.pi / 1) * servo1_angle2_time + math.pi))
            servo1.move(servo1_angle2, 100)
            print(f"Servo 1 is at {servo1_angle2} degrees. At min.")
            servo2_angle2_time = 0.27481818199157715
            servo2_angle2 = 88.80 + (20 * math.sin((2 * math.pi / 1) * servo2_angle2_time + math.pi))
            servo2.move(servo2_angle2, 100)
            print(f"Servo 2 is at {servo2_angle2} degrees. At max.")
            servo5_angle2_time = 0.2665979862213135
            servo5_angle2 = 115.44 + (20 * math.sin((2 * math.pi / 1) * servo5_angle2_time + math.pi))
            servo5.move(servo5_angle2, 100)
            print(f"Servo 5 is at {servo5_angle2} degrees. At min.")
            servo6_angle2_time = 0.26810288429260254
            servo6_angle2 = 172.80 + (20 * math.sin((2 * math.pi / 1) * servo6_angle2_time + math.pi))
            servo6.move(servo6_angle2, 100)
            print(f"Servo 6 is at {servo6_angle2} degrees. At max.\n")
            time.sleep(0.2)

            print("Front and back legs from point 1 to point 2.\n")
            
            # Move left and right legs from start to point 1 - moving knee to max, ankle to min
            servo3_angle1_time = 0.1106269359588623
            servo3_angle1 = 133.68 + (20 * math.sin((2 * math.pi / 1) * servo3_angle1_time + math.pi))
            servo3.move(servo3_angle1, 100)
            print(f"Servo 3 is at {servo3_angle1} degrees. Moving to min.")
            servo4_angle1_time = 0.11086916923522949
            servo4_angle1 = 153.84 + (20 * math.sin((2 * math.pi / 1) * servo4_angle1_time + 0))
            servo4.move(servo4_angle1, 100)
            print(f"Servo 4 is at {servo4_angle1} degrees. Moving to max.")
            servo7_angle1_time = 0.11015701293945312
            servo7_angle1 = 130.56 + (20 * math.sin((2 * math.pi / 1) * servo7_angle1_time + math.pi))
            servo7.move(servo7_angle1, 100)
            print(f"Servo 7 is at {servo7_angle1} degrees. Moving to min.")
            servo8_angle1_time = 0.10747408866882324
            servo8_angle1 = 121.20 + (20 * math.sin((2 * math.pi / 1) * servo8_angle1_time + 0))
            servo8.move(servo8_angle1, 100) 
            print(f"Servo 8 is at {servo8_angle1} degrees. Moving to max.\n")  
            time.sleep(0.2)

            print("Left and right legs from start to point 1.\n")

            # Move left and right legs from point 1 to point 2 - knee at max, ankle at min
            servo3_angle2_time = 0.27266383171081543
            servo3_angle2 = 133.68 + (20 * math.sin((2 * math.pi / 1) * servo3_angle2_time + math.pi))
            servo3.move(servo3_angle2, 100)
            print(f"Servo 3 is at {servo3_angle2} degrees. At min.")
            servo4_angle2_time = 0.27592897415161133
            servo4_angle2 = 153.84 + (20 * math.sin((2 * math.pi / 1) * servo4_angle2_time + 0))
            servo4.move(servo4_angle2, 100)
            print(f"Servo 4 is at {servo4_angle2} degrees. At max.")
            servo7_angle2_time = 0.27532005310058594
            servo7_angle2 = 130.56 + (20 * math.sin((2 * math.pi / 1) * servo7_angle2_time + math.pi))
            servo7.move(servo7_angle2, 100)
            print(f"Servo 7 is at {servo7_angle2} degrees. At min.")
            servo8_angle2_time = 0.26618003845214844
            servo8_angle2 = 121.20 + (20 * math.sin((2 * math.pi / 1) * servo8_angle2_time + 0))
            servo8.move(servo8_angle2, 100) 
            print(f"Servo 8 is at {servo8_angle2} degrees. At max.\n")  
            time.sleep(0.2)

            print("Left and right legs from point 1 to point 2.\n")

            # Move front and back legs from point 2 to point 3 - moving knee to min, ankle to max 
            servo1_angle3_time = 0.428757905960083
            servo1_angle3 = 147.36 + (20 * math.sin((2 * math.pi / 1) * servo1_angle3_time + math.pi))
            servo1.move(servo1_angle3, 100)
            print(f"Servo 1 is at {servo1_angle3} degrees. Moving to max.")
            servo2_angle3_time = 0.4398972988128662
            servo2_angle3 = 88.80 + (20 * math.sin((2 * math.pi / 1) * servo2_angle3_time + math.pi))
            servo2.move(servo2_angle3, 100)
            print(f"Servo 2 is at {servo2_angle3} degrees. Moving to min.")
            servo5_angle3_time = 0.4318418502807617
            servo5_angle3 = 115.44 + (20 * math.sin((2 * math.pi / 1) * servo5_angle3_time + math.pi))
            servo5.move(servo5_angle3, 100)
            print(f"Servo 5 is at {servo5_angle3} degrees. Moving to max.")
            servo6_angle3_time = 0.4280240535736084
            servo6_angle3 = 172.80 + (20 * math.sin((2 * math.pi / 1) * servo6_angle3_time + math.pi))
            servo6.move(servo6_angle3, 100)
            print(f"Servo 6 is at {servo6_angle3} degrees. Moving to min.\n")
            time.sleep(0.2)

            print("Front and back legs from point 2 to point 3.\n")

            # Move front and back legs from point 3 to point 4 - moving knee to min, ankle to max 
            servo1_angle4_time = 0.5904650688171387
            servo1_angle4 = 147.36 + (20 * math.sin((2 * math.pi / 1) * servo1_angle4_time + math.pi))
            servo1.move(servo1_angle4, 100)
            print(f"Servo 1 is at {servo1_angle4} degrees. Moving to max.")
            servo2_angle4_time = 0.6025242805480957
            servo2_angle4 = 88.80 + (20 * math.sin((2 * math.pi / 1) * servo2_angle4_time + math.pi))
            servo2.move(servo2_angle4, 100)
            print(f"Servo 2 is at {servo2_angle4} degrees. Moving to min.")
            servo5_angle4_time = 0.595344066619873
            servo5_angle4 = 115.44 + (20 * math.sin((2 * math.pi / 1) * servo5_angle4_time + math.pi))
            servo5.move(servo5_angle4, 100)
            print(f"Servo 5 is at {servo5_angle4} degrees. Moving to max.")
            servo6_angle4_time = 0.5887000560760498
            servo6_angle4 = 172.80 + (20 * math.sin((2 * math.pi / 1) * servo6_angle4_time + math.pi))
            servo6.move(servo6_angle4, 100)
            print(f"Servo 6 is at {servo6_angle4} degrees. Moving to min.\n")
            time.sleep(0.2)

            print("Front and back legs from point 3 to point 4.\n")

            # Move front and back legs from point 4 to point 5 - knee at min, ankle at max
            servo1_angle5_time = 0.7522311210632324
            servo1_angle5 = 147.36 + (20 * math.sin((2 * math.pi / 1) * servo1_angle5_time + math.pi))
            servo1.move(servo1_angle5, 100)
            print(f"Servo 1 is at {servo1_angle5} degrees. At max.")
            servo2_angle5_time = 0.7676851749420166
            servo2_angle5 = 88.80 + (20 * math.sin((2 * math.pi / 1) * servo2_angle5_time + math.pi))
            servo2.move(servo2_angle5, 100)
            print(f"Servo 2 is at {servo2_angle5} degrees. At min.")
            servo5_angle5_time = 0.757112979888916
            servo5_angle5 = 115.44 + (20 * math.sin((2 * math.pi / 1) * servo5_angle5_time + math.pi))
            servo5.move(servo5_angle5, 100)
            print(f"Servo 5 is at {servo5_angle5} degrees. At max.")
            servo6_angle5_time = 0.750373125076294
            servo6_angle5 = 172.80 + (20 * math.sin((2 * math.pi / 1) * servo6_angle5_time + math.pi))
            servo6.move(servo6_angle5, 100)
            print(f"Servo 6 is at {servo6_angle5} degrees. At min.\n")
            time.sleep(0.2)

            print("Front and back legs from point 4 to point 5.\n")
            
            # Move left and right legs from point 2 to point 3 - moving knee to min, ankle to max
            servo3_angle3_time = 0.4369039535522461
            servo3_angle3 = 133.68 + (20 * math.sin((2 * math.pi / 1) * servo3_angle3_time + math.pi))
            servo3.move(servo3_angle3, 100)
            print(f"Servo 3 is at {servo3_angle3} degrees. Moving to max.")
            servo4_angle3_time = 0.4353969097137451
            servo4_angle3 = 153.84 + (20 * math.sin((2 * math.pi / 1) * servo4_angle3_time + 0))
            servo4.move(servo4_angle3, 100)
            print(f"Servo 4 is at {servo4_angle3} degrees. Moving to min.")
            servo7_angle3_time = 0.43543124198913574
            servo7_angle3 = 130.56 + (20 * math.sin((2 * math.pi / 1) * servo7_angle3_time + math.pi))
            servo7.move(servo7_angle3, 100)
            print(f"Servo 7 is at {servo7_angle3} degrees. Moving to max.")
            servo8_angle3_time = 0.42971205711364746
            servo8_angle3 = 121.20 + (20 * math.sin((2 * math.pi / 1) * servo8_angle3_time + 0))
            servo8.move(servo8_angle3, 100) 
            print(f"Servo 8 is at {servo8_angle3} degrees. Moving to min.\n")  
            time.sleep(0.2)

            print("Left and right legs from point 2 to point 3.\n")
            
            # Move left and right legs from point 3 to point 4 - moving knee to min, ankle to max 
            servo3_angle4_time = 0.5945649147033691
            servo3_angle4 = 133.68 + (20 * math.sin((2 * math.pi / 1) * servo3_angle4_time + math.pi))
            servo3.move(servo3_angle4, 100)
            print(f"Servo 3 is at {servo3_angle4} degrees. Moving to max.")
            servo4_angle4_time = 0.5962309837341309
            servo4_angle4 = 153.84 + (20 * math.sin((2 * math.pi / 1) * servo4_angle4_time + 0))
            servo4.move(servo4_angle4, 100)
            print(f"Servo 4 is at {servo4_angle4} degrees. Moving to min.")
            servo7_angle4_time = 0.5980091094970703
            servo7_angle4 = 130.56 + (20 * math.sin((2 * math.pi / 1) * servo7_angle4_time + math.pi))
            servo7.move(servo7_angle4, 100)
            print(f"Servo 7 is at {servo7_angle4} degrees. Moving to max.")
            servo8_angle4_time = 0.5912811756134033
            servo8_angle4 = 121.20 + (20 * math.sin((2 * math.pi / 1) * servo8_angle4_time + 0))
            servo8.move(servo8_angle4, 100) 
            print(f"Servo 8 is at {servo8_angle4} degrees. Moving to min.\n")  
            time.sleep(0.2)

            print("Left and right legs from point 3 to point 4.\n")

            # Move left and right legs from point 4 to point 5 - knee at min, ankle at max 
            servo3_angle5_time = 0.7569999694824219
            servo3_angle5 = 133.68 + (20 * math.sin((2 * math.pi / 1) * servo3_angle5_time + math.pi))
            servo3.move(servo3_angle5, 100)
            print(f"Servo 3 is at {servo3_angle5} degrees. At max.")
            servo4_angle5_time = 0.756140947341919
            servo4_angle5 = 153.84 + (20 * math.sin((2 * math.pi / 1) * servo4_angle5_time + 0))
            servo4.move(servo4_angle5, 100)
            print(f"Servo 4 is at {servo4_angle5} degrees. At min.")
            servo7_angle5_time = 0.7599022388458252
            servo7_angle5 = 130.56 + (20 * math.sin((2 * math.pi / 1) * servo7_angle5_time + math.pi))
            servo7.move(servo7_angle5, 100)
            print(f"Servo 7 is at {servo7_angle5} degrees. At max.")
            servo8_angle5_time = 0.7530090808868408
            servo8_angle5 = 121.20 + (20 * math.sin((2 * math.pi / 1) * servo8_angle5_time + 0))
            servo8.move(servo8_angle5, 100) 
            print(f"Servo 8 is at {servo8_angle5} degrees. At min.\n")  
            time.sleep(0.2)

            print("Left and right legs from point 4 to point 5.\n")
    
            # Move front and back legs from point 5 to point 6 - moving to home 
            servo1_angle6_time = 0.9133250713348389
            servo1_angle6 = 147.36 + (20 * math.sin((2 * math.pi / 1) * servo1_angle6_time + math.pi))
            servo1.move(servo1_angle6, 100)
            print(f"Servo 1 is at {servo1_angle6} degrees. Moving to home.")
            servo2_angle6_time = 0.9328901767730713
            servo2_angle6 = 88.80 + (20 * math.sin((2 * math.pi / 1) * servo2_angle6_time + math.pi))
            servo2.move(servo2_angle6, 100)
            print(f"Servo 2 is at {servo2_angle6} degrees. Moving to home.")
            servo5_angle6_time = 0.9204530715942383
            servo5_angle6 = 115.44 + (20 * math.sin((2 * math.pi / 1) * servo5_angle6_time + math.pi))
            servo5.move(servo5_angle6, 100)
            print(f"Servo 5 is at {servo5_angle6} degrees. Moving to home.")
            servo6_angle6_time = 0.9071481227874756
            servo6_angle6 = 172.80 + (20 * math.sin((2 * math.pi / 1) * servo6_angle6_time + math.pi))
            servo6.move(servo6_angle6, 100)
            print(f"Servo 6 is at {servo6_angle6} degrees. Moving to home.\n")
            time.sleep(0.2)

            print("Front and back legs from point 5 to point 6.\n")

            # Move front and back legs from point 6 to home - at home 
            servo1_angle7_time = 0.00032210350036621094
            servo1_angle7 = 147.36 + (20 * math.sin((2 * math.pi / 1) * servo1_angle7_time + math.pi))
            servo1.move(servo1_angle7, 100)
            print(f"Servo 1 is at {servo1_angle7} degrees. At home.")
            servo2_angle7_time = 0.0001742839813232422
            servo2_angle7 = 88.80 + (20 * math.sin((2 * math.pi / 1) * servo2_angle7_time + math.pi))
            servo2.move(servo2_angle7, 100)
            print(f"Servo 2 is at {servo2_angle7} degrees. At home.")
            servo5_angle7_time = 0.00019097328186035156
            servo5_angle7 = 115.44 + (20 * math.sin((2 * math.pi / 1) * servo5_angle7_time + math.pi))
            servo5.move(servo5_angle7, 100)
            print(f"Servo 5 is at {servo5_angle7} degrees. At home.")
            servo6_angle7_time = 0.00019884109497070312
            servo6_angle7 = 172.80 + (20 * math.sin((2 * math.pi / 1) * servo6_angle7_time + math.pi))
            servo6.move(servo6_angle7, 100)
            print(f"Servo 6 is at {servo6_angle7} degrees. At home.\n")
            time.sleep(0.2)

            print("Front and back legs from point 6 to home.\n")
            
            # Move left and right legs from point 5 to point 6 - moving to home 
            servo3_angle6_time = 0.9208850860595703
            servo3_angle6 = 133.68 + (20 * math.sin((2 * math.pi / 1) * servo3_angle6_time + math.pi))
            servo3.move(servo3_angle6, 100)
            print(f"Servo 3 is at {servo3_angle6} degrees. Moving to home.")
            servo4_angle6_time = 0.9185879230499268
            servo4_angle6 = 153.84 + (20 * math.sin((2 * math.pi / 1) * servo4_angle6_time + 0))
            servo4.move(servo4_angle6, 100)
            print(f"Servo 4 is at {servo4_angle6} degrees. Moving to home.")
            servo7_angle6_time = 0.9242391586303711
            servo7_angle6 = 130.56 + (20 * math.sin((2 * math.pi / 1) * servo7_angle6_time + math.pi))
            servo7.move(servo7_angle6, 100)
            print(f"Servo 7 is at {servo7_angle6} degrees. Moving to home.")
            servo8_angle6_time = 0.9078829288482666
            servo8_angle6 = 121.20 + (20 * math.sin((2 * math.pi / 1) * servo8_angle6_time + 0))
            servo8.move(servo8_angle6, 100) 
            print(f"Servo 8 is at {servo8_angle6} degrees. Moving to home.\n")  
            time.sleep(0.2)

            print("Left and right legs fromt point 5 to point 6.\n")
    
            # Move left and right legs from point 6 to home - at home 
            servo3_angle7_time = 0.00019311904907226562
            servo3_angle7 = 133.68 + (20 * math.sin((2 * math.pi / 1) * servo3_angle7_time + math.pi))
            servo3.move(servo3_angle7, 100)
            print(f"Servo 3 is at {servo3_angle7} degrees. At home.")
            servo4_angle7_time = 0.0002048015594482422
            servo4_angle7 = 153.84 + (20 * math.sin((2 * math.pi / 1) * servo4_angle7_time + 0))
            servo4.move(servo4_angle7, 100)
            print(f"Servo 4 is at {servo4_angle7} degrees. At home.")
            servo7_angle7_time = 0.0002048015594482422
            servo7_angle7 = 130.56 + (20 * math.sin((2 * math.pi / 1) * servo7_angle7_time + math.pi))
            servo7.move(servo7_angle7, 100)
            print(f"Servo 7 is at {servo7_angle7} degrees. At home.")
            servo8_angle7_time = 0.00018405914306640625
            servo8_angle7 = 121.20 + (20 * math.sin((2 * math.pi / 1) * servo8_angle7_time + 0))
            servo8.move(servo8_angle7, 100) 
            print(f"Servo 8 is at {servo8_angle7} degrees. At home.\n")  
            time.sleep(0.2)

            print("Left and right legs fromt point 5 to point 6.\n")

            print(f"\nOne step completed.\n")

    except ServoArgumentError as e:
        print(f"Servo {e.id_} is outside the range 0 - 240 degrees or outside the range set by LX16A.set_angle_limits")
    except ServoLogicalError as e:
        print(f"The command is issued while in motor mode or while torque is disabled")
        
# Function to begin backwards motion
def backward_motion():
    print("Begin backwards motion.\n")
    try:    
       for _ in range(3):
           
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
        
        # Use pyaudio for more control over audio stream
        audio_stream = recognizer.listen(source, timeout=20)  # Timeout set to 20 seconds

    try:
        print("Command recognized.\n")
        command = recognizer.recognize_google(audio_stream)
        print("Command:", command)
        process_command(command)
    except sr.UnknownValueError:
        print("\nCould not understand audio")
    except sr.RequestError as e:
        print("\nCould not request results; {0}".format(e))

# Function to detect audio activity (e.g., noise)
def detect_audio_activity():
    with sr.Microphone() as source:
        print("Listening for audio activity...\n")
        recognizer.adjust_for_ambient_noise(source)
        
        # Use pyaudio to stream audio and detect noise
        audio_stream = source.stream
        audio_data = audio_stream.read(1024)  # Read a chunk of audio data
        audio_level = max(audio_data)  # Check the maximum audio level in the chunk

        # If audio level exceeds a certain threshold, wake up
        if audio_level > 50:
            print("Audio activity detected.")
            return True
        else:
            return False

# Main loop
while True:
    if detect_audio_activity():
        listen_for_commands()