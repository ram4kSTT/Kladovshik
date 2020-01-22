#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here
brick.sound.beep()

leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)
grabMotor = Motor(Port.D)
colorSensorGruz = ColorSensor(Port.S1)
colorSensorRight = ColorSensor(Port.S2)
colorSensorLeft = ColorSensor(Port.S3)
directionRotation = 1
directionGrab = 1
Const_turn_Angle = 400
Const_turn_Speed_Left = 50
Const_turn_Speed_Right = -50
Const_Razvorot_Angle = 180
Const_Razvorot_Speed_Left = 200
Const_Razvorot_Speed_Right = 200
Const_Grab_Speed = 200
Const_Grab_angle = 150
Const_Go_Speed_Left = 200
Const_Go_Speed_Right = 200
Const_Relection_Limit = 20
Const_Speed_Fline = 20
Const_Slow_Speed_Fline = 50
Const_MotorRule_Speed = 150
directionTurn = 1
xRobot = 2
yRobot = 0
xPlatform = 0
yPlatform = 0

##################################################################################
ColorMap = [
    [Color.RED,Color.YELLOW,Color.GREEN],
    [Color.GREEN,Color.RED,Color.BLUE]
    ]
#####################################################################################

def turn(directionTurn):
    leftMotor.reset_angle(0)
    leftMotor.dc(Const_turn_Speed_Left * directionRotation* directionTurn)
    rightMotor.dc(Const_turn_Speed_Right * directionRotation* directionTurn)
    while(True):
        angle = leftMotor.angle()
        if(angle == Const_turn_Angle):
            leftMotor.stop()
            rightMotor.stop()
            break
def razovorot():
    leftMotor.reset_angle(0)
    leftMotor.dc(Const_turn_Speed_Left * directionRotation * directionRazvorot)
    rightMotor.dc(Const_turn_Speed_Right * directionRotation * directionRazvorot)
    while(True):
        angle = leftMotor.angle()
        if(angle == Const_Razvorot_Angle):
            leftMotor.stop()
            rightMotor.stop()
            break
def grab():
  grabMotor.reset_angle(0)
  grabMotor.dc(Const_Grab_Speed * directionGrab)
  while(True):
        grabMotor.angle()
        angleGrab = grabMotor.angle()
        if(angleGrab == Const_Grab_angle ):
            grabMotor.stop()
            break

#езда по черной линии
#crossroadCounts - кол-во перекрестков, которые необходимо проехать
def motorRule(left,right):
    leftMotor.run(Const_MotorRule_Speed * directionRotation)
    rightMotor.run(Const_MotorRule_Speed * directionRotation)

#езда по черной линии
#crossroadCounts - кол-во перекрестков, которые необходимо проехать
def fLine(crossroadCounts):
    colors = [Color.GREEN,Color.RED,Color.BLUE,Color.BROWN]
    colorCounts = 0
    crossroad = 0
    blackLine = False
    while(True):
      reflectionLEFT = colorSensorLeft.reflection()
      reflectionRight = colorSensorRight.reflection()

      if(reflectionLEFT < Const_Relection_Limit):
        if(reflectionRight < Const_Relection_Limit):
          motorRule(Const_Speed_Fline,Const_Speed_Fline)
        else:
          motorRule(-Const_Slow_Speed_Fline,Const_Slow_Speed_Fline)
      else:
        if(reflectionRight < Const_Relection_Limit):
          motorRule(Const_Slow_Speed_Fline,-Const_Slow_Speed_Fline)
        else:
          motorRule(Const_Speed_Fline,Const_Speed_Fline)
      
      if((reflectionLEFT < Const_Relection_Limit) & (reflectionRight < Const_Relection_Limit)):
        if(blackLine == False):
          crossroad = crossroad + 1
          if(crossroad == crossroadCounts):
            motorRule(0,0)
            break
        blackLine = True
      else:
        blackLine = False
      color = colorSensorGruz.color()
      if(color in colors):
        print(color)
        colorCounts = colorCounts + 1
        if(colorCounts > 0):
          motorRule(0,0)
          break



def logic():
  povorot = 0
  countsBlackCrossroad =abs(xRobot - xPlatform)
  robotWay = [["grab", 1], ["razovorot", 0 ],["fLine",1] ]
  if(yRobot == 0):
    directionRotation * -1 
  if(xRobot - xPlatform  == -1) or (xRobot - xPlatform  == -2):
   povorot = -1
  else:
    povorot = 1
  
  
  if(xRobot - xPlatform  == -1) or (xRobot - xPlatform  == -2) and (yPlatform == 0):
    povorot = -1
    
  elif(xRobot - xPlatform  == -1) or (xRobot - xPlatform  == -2) and (yPlatform == 1):
    povorot = 1
  
  elif(xRobot - xPlatform  == 1) or (xRobot - xPlatform  == 2) and (yPlatform == 0):
    povorot = -1
   
  elif(xRobot - xPlatform  == -1) or (xRobot - xPlatform  == -2) and (yPlatform == 1):
    povorot = 1
  elif(xRobot == xPlatform) and (yRobot == yPlatform):
    robotWay.append(["MotorRule",2])
    robotWay.append(["razovorot",0])
    robotWay.append(["fLine",1])
  elif(xRobot == xPlatform):
    robotWay.append(["MotorRule",0])
  
  robotWay.append(["turn", povorot])
  robotWay.append(["fLine",countsBlackCrossroad])
  robotWay.append(["turn", povorot])
  return robotWay


def perfomer(robotWay):
  for way in robotWay:
    if(way[0] == "turn"):
      turn(way[1])
    elif(way[0] == "razovorot"):
      razovorot(way[1])
    elif(way[0] == "fLine"):
      fLine(way[1])
    elif(way[0] == "grab"):
      grab()


perfomer(logic())



    



