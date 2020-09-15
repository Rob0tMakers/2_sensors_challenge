import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


class Robot:
	def __init__(self):
		# micro controller
		ev3 = EV3Brick()
		ev3.speaker.beep()
		# sensors
		# low value = registers black tape
		# high value = aluminum
		self.sensorYellow = ColorSensor(Port.S1)
		self.sensorRed = ColorSensor(Port.S3)
		self.sensorBlue = ColorSensor(Port.S2)
		# motor
		left_motor = Motor(Port.A, gears=[40, 24])
		right_motor = Motor(Port.B, gears=[40, 24])
		axle_track = 205
		wheel_diameter = 35
		self.motors = DriveBase(left_motor, right_motor,
														wheel_diameter, axle_track)
		# constants

		# intersection detection of side sensors
		self.thresholdBlueSensor = 30

		# value for making turns
		self.thresholdSideSensors = 15

		# timer

		self.watch = StopWatch()
		self.timer = 0

	def drive(self, directions):
		i = 0
		while i < len(directions):
			self.timer = self.watch.time()
			if self.timer % 100 == 0:
				print(self.timer)
			self.correctPath()

			if self.senseIntersection() == True and self.timer >= 500:
				print('intersection')
				self.motors.drive_time(0, 0, 1000) # reduce this when done
				self.executeCommand(directions[i])
				i += 1

			self.motors.drive(-125, 0)


	def executeCommand(self, cmd):
		if cmd == 0:
			print('straight')
			self.driveStraight()

		if cmd == 1:
			print('right')
			self.turnRight()

		if cmd == 2:
			print('left')
			self.turnLeft()

		if cmd == 3:
			print('reverse')
			self.reverse()

		if cmd == 4:
			print('stop')

	# turning behaviours at intersection

	def turnLeft(self):
		self.motors.drive_time(-30, 44, 2000)
		self.watch.reset()

	def turnRight(self):
		self.motors.drive_time(-30, -46, 2000)
		self.watch.reset()

	def driveStraight(self):
		self.motors.drive_time(-60, 0, 1800)
		self.watch.reset()

	def reverse(self):
		self.motors.drive_time(60, 0, 1800)
		self.motors.drive_time(0, 94, 2000)
		self.motors.drive_time(-60, 0, 800)

	# intersection detection

	def senseIntersection(self):
		if self.sensorRed.reflection() < 2 or self.sensorYellow.reflection() < 2:
			return True

	# path correction

	# completely aluminum = 23
	# completely black tape = 1
	def correctPath(self):
		if self.sensorBlue.reflection() < 8:
			self.adjustLeft()

		if self.sensorBlue.reflection() > 16:
			self.adjustRight()

	# default: -125, angle
	def adjustLeft(self):
		angle = 12 - min(self.sensorBlue.reflection(), 10)
		step = 125 + (12 - min(self.sensorBlue.reflection(), 10))
		self.motors.drive(-step, angle)

	def adjustRight(self):
		angle = max(self.sensorBlue.reflection(), 14) -12
		step = 125 + (max(self.sensorBlue.reflection(), 14) -12)
		self.motors.drive(-step, -angle)