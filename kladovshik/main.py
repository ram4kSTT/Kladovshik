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
Const_turn_Angle = 155
Const_turn_Speed = 50
Const_Razvorot_Angle = 330
Const_Razvorot_Speed = 50
Const_Grab_Speed = 200
Const_Grab_angle = 150
Const_Go_Speed = 200
Const_Relection_Limit = 20
Const_Speed_Fline = 20
Const_Slow_Speed_Fline = 50
Const_MotorRule_Speed = 150
Robot = [2,0]
Platform = [0,0]

##################################################################################
ColorMap = [
    [Color.RED,Color.YELLOW,Color.GREEN],
    [Color.GREEN,Color.RED,Color.BLUE]
    ]
#####################################################################################
#разварачиваемся на 90 градусов
#directionTurn - выбор направления поворота  значение может быть 1 (направо) или -1 (налево)
def turn(directionTurn):
  print("turn:")
  print(directionTurn)
  leftMotor.reset_angle(0)
  leftMotor.dc(Const_turn_Speed *  directionTurn)
  rightMotor.dc(-Const_turn_Speed *  directionTurn)
  while(True):
      angle = abs(leftMotor.angle())
      if(angle >= Const_turn_Angle):
          leftMotor.stop()
          rightMotor.stop()
          break
#разварачиваемся на 180 градусов
def razovorot():
  print("разворачиваемся")
  leftMotor.reset_angle(0)
  leftMotor.dc(Const_turn_Speed)
  rightMotor.dc(-Const_turn_Speed)
  while(True):
      angle = abs(leftMotor.angle())
      if(angle >= Const_Razvorot_Angle):
          leftMotor.stop()
          rightMotor.stop()
          break
          


#захват кубика манипулятором
def grab():
  print("захватываем кубик")
  grabMotor.reset_angle(0)
  grabMotor.dc(Const_Grab_Speed)
  while(True):
    grabMotor.angle()
    angleGrab = grabMotor.angle()
    if(angleGrab >= Const_Grab_angle ):
        print("кубик")
        grabMotor.stop()
        return



#езда по черной линии
#left - мощность левого мотора
#right - мощность правого мотора
def motorRule(left,right):
    leftMotor.run(left)
    rightMotor.run(right)



#езда по черной линии
#crossroadCounts - кол-во перекрестков, которые необходимо проехать
def fLine(crossroadCounts):
  print("fLine:")
  print(crossroadCounts)

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
#определяет путь от местоположение робота до нужной платформы
def logic():
  print("logic:")
  print("рассчитываем путь")
  povorot2 = 0
  povorot1 = 1
  countsBlackCrossroad =abs(Robot[0] - Platform[0])
  robotWay = [["grab", 1], ["razovorot", 0 ],["fLine",1] ]
  
  if(Robot[1] == 0):
    povorot1 * -1 
  if(Robot[0] - Platform[0]  == -1) or (Robot[0] - Platform[0]  == -2):
   povorot2 = -1
  else:
    povorot2 = 1
  if(Robot[0] - Platform[0]  == -1) or (Robot[0] - Platform[0]  == -2) and (Platform[1] == 0):
    povorot2 = -1
  elif(Robot[0] - Platform[0]  == -1) or (Robot[0] - Platform[0]  == -2) and (Platform[1] == 1):
    povorot2 = 1
  elif(Robot[0] - Platform[0]  == 1) or (Robot[0] - Platform[0]  == 2) and (Platform[1] == 0):
    povorot2 = -1
  elif(Robot[0] - Platform[0]  == -1) or (Robot[0] - Platform[0]  == -2) and (Platform[1] == 1):
    povorot2 = 1
  elif(Robot[0] == Platform[0]) and (Robot[1] == Platform[1]):
    robotWay.append(["MotorRule",2])
    robotWay.append(["razovorot",0])
    robotWay.append(["fLine",1])
  elif(Robot[0] == Platform[0]):
    robotWay.append(["MotorRule",0])
  robotWay.append(["turn", povorot1])
  robotWay.append(["fLine",countsBlackCrossroad])
  robotWay.append(["turn", povorot2])
  return robotWay

#проезжает от местоположения робота до нужной платформы
#robotWay - инструкция как доехать от местоположения робота до нужной платформы
def perfomer(robotWay):
  print("perfomer:")
  print(robotWay)
  for way in robotWay:
    if(way[0] == "turn"):
      turn(way[1])
    elif(way[0] == "razovorot"):
      razovorot()
    elif(way[0] == "fLine"):
      fLine(way[1])
    elif(way[0] == "grab"):
      grab()



perfomer(logic())