#!/usr/bin/env pybricks-micropython
from robot import Robot

# 0 straight, 1 right, 2 left, 3 reverse, 4 stop
taskList = [2,0,0,3,2,2,2,0,3,1,0,0,2,0,2,0,0,3,1,2,0,4]
# taskList = [0,0,4]

robot = Robot()

robot.drive(taskList)
