#!/usr/bin/env python3

import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version      # initializes the simulation and creates it 
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally          # gives the path for your robot 
p.setGravity(0,0,-9.81)                                                     # sets gravity --> pybullet uses the metric system 
groundId = p.loadURDF("plane.urdf")                                         # put objects in this world --> ground/floor --> imports as URDF and assign it to a variable 
robotStartPos = [0,0,1]                                                     # robot starting position
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])                   # loads the robot at default position
robotId = p.loadURDF("myrobot.urdf",robotStartPos, robotStartOrientation)    # loads the robot at a desired position and orientation
for i in range (10000):                                                     # loop that steps the simulator
    p.stepSimulation()                                                      # step the simulation 10,000 times
    time.sleep(1./240.)                                                     # sleeps the computer 
    # may need to indent these next two lines   
robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)               # where did the robot end uo    
print(robotPos, robotOrn)                                                   # gives you robot position and orientation
p.disconnect()                                                              # shuts down the simulation 