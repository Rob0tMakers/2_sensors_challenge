#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
sensorYellow = ColorSensor(Port.S1)
sensorRed = ColorSensor(Port.S2)
sensorBlue = ColorSensor(Port.S3)

left_motor = Motor(Port.A, gears=[40, 24])
right_motor = Motor(Port.B, gears=[40, 24])

axle_track = 159
wheel_diameter = 35

robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

# Write your program here.
ev3.speaker.beep()

while True:
    while sensorBlue.reflection() < 5:
        print("yellow: " + str(sensorYellow.reflection()))
        print("red: " + str(sensorRed.reflection()))
        print("blue: " + str(sensorBlue.reflection()))
        print("\n")
        robot.drive(150, 0)

    if sensorRed.reflection() < 5:
        # turn left
        while sensorRed.reflection() < 5:
            robot.drive_time(0, -100, 500)
            wait(1000)

    if sensorYellow.reflection() < 5:
        # turn right
        ev3.speaker.beep()
        robot.drive_time(0, 0, 1000)
        robot.drive_time(150, 0, 200)
        while sensorYellow.reflection() < 5:
            robot.drive_time(0, 100, 500)
            wait(1000)
