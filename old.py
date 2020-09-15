#!/usr/bin/env pybricks-micropython
import random
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# bug: opposing sensors blocks turn before turn completion??

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

path = [0, 1, 2, 2, 2, 2, 1, 0, 1, 1]  # Figure 8
# path = [2, 1, 0]  # crossroads test
# 0 straight, 1 right, 2 left, 3 reverse

# Create your objects here.
ev3 = EV3Brick()
sensorYellow = ColorSensor(Port.S1)
sensorRed = ColorSensor(Port.S3)
sensorBlue = ColorSensor(Port.S2)

left_motor = Motor(Port.A, gears=[40, 24])
right_motor = Motor(Port.B, gears=[40, 24])

axle_track = 159
wheel_diameter = 35

motors = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

# Write your program here.
ev3.speaker.beep()

speed_d = 150
speed_t = 800
i = 0


def turnLeft():
  motors.drive_time(150, 0, 400)
  motors.drive_time(0, -90, 200)
  # while sensorRed.reflection() < 5 or sensorBlue.reflection() > 5:
  while sensorBlue.reflection() > 15:
    motors.drive_time(0, -50, 200)
  global i
  i += 1


def adjustLeft():
  while sensorRed.reflection() < 30 or sensorBlue.reflection() > 30:
    motors.drive_time(0, -30, 200)


def turnRight():
  motors.drive_time(150, 0, 400)
  motors.drive_time(0, 90, 200)
  # while sensorYellow.reflection() < 5 or sensorBlue.reflection() > 5:
  while sensorBlue.reflection() > 15:
    motors.drive_time(0, 50, 200)
  global i
  i += 1


def adjustRight():
  while sensorRed.reflection() < 30 or sensorBlue.reflection() > 30:
    motors.drive_time(0, 30, 200)


def sensorCheck():
  print()
  print("yellow: " + str(sensorYellow.reflection()))
  print("red: " + str(sensorRed.reflection()))
  print("blue: " + str(sensorBlue.reflection()))


while True:
  while sensorBlue.reflection() < 15:  # Is motors on a path
    motors.drive(200, 0)

    # T intersection
    if sensorRed.reflection() < 15 and sensorYellow.reflection() < 15:
      sensorCheck()
      print('crossroads')
      choice = path[i]
      #choice = random.randrange(0, 3)
      if choice == 0:
        print('straight')
        motors.drive_time(speed_d, 0, speed_t)
        i += 1
      if choice == 1:
        print('right')
        turnRight()
      if choice == 2:
        print('left')
        turnLeft()

      # Y intersection to left
    elif sensorRed.reflection() < 15:
      sensorCheck()
      print('angled left')
      choice = path[i]
      #choice = random.randrange(0, 2)
      if choice == 0:
        print('straight')
        motors.drive_time(speed_d, 0, speed_t)
        i += 1
      if choice == 2:
        print('left')
        turnLeft()

    # Y intersection to the right
    elif sensorYellow.reflection() < 15:
      sensorCheck()
      print('angled right')
      choice = path[i]
      #choice = random.randrange(0, 2)
      if choice == 0:
        print('straight')
        motors.drive_time(speed_d, 0, speed_t)
        i += 1
      if choice == 1:
        print('right')
        turnRight()

  # path correction

  # turn left
  if sensorRed.reflection() < 30:
    # debugging
    ev3.speaker.beep()
    adjustLeft()

  # turn right
  if sensorYellow.reflection() < 30:
    # debugging
    ev3.speaker.beep()
    adjustRight()

  if sensorRed.reflection() > 15 and sensorYellow.reflection() > 15 and sensorBlue.reflection() > 15:
    motors.drive_time(0, 50, 200)
