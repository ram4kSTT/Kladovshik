from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here
brick.sound.beep()
#################################################################################################################
# переменные и константы
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)
grabMotor = Motor(Port.D)
colorSensorGruz = ColorSensor(Port.S1)
colorSensorRight = ColorSensor(Port.S2)
colorSensorLeft = ColorSensor(Port.S3)
directionRotation = 1
Const_turn_Angle = 400
Const_turn_Speed_Left = 200
Const_turn_Speed_Right = -200
Const_Razvorot_Angle = 180
Const_Razvorot_Speed = 200
##################################################################################################################
def turn():
    Const_turn_Speed_Left * directionRotation
    Const_turn_Speed_Right * directionRotation
    leftMotor.duty(Const_turn_Speed_Left)
    rightMotor.duty(Const_turn_Speed_Right)

turn()