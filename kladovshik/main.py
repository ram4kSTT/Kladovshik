#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

import platform as pl
import time
# Write your program here


leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)
grabMotor = Motor(Port.A)

colorSensorGruz = ColorSensor(Port.S1)
colorSensorRight = ColorSensor(Port.S2)
colorSensorLeft = ColorSensor(Port.S3)
gyroSensor = GyroSensor(Port.S4)

Const_turn_Angle = 80
Const_turn_Speed = 150
Const_Razvorot_Angle = 160
Const_Grab_Speed = 25
Const_Grab_angle = 140
Const_Go_Speed = 200
Const_Relection_Limit = 15
Const_Speed_Fline = 250
Const_Slow_Speed_Fline_Big= 150
Const_Slow_Speed_Fline_Small = -50
Const_MotorRule_Speed = 150
Const_checkColor_Speed = 50
Const_Go_Forward_Speed = 300
Const_Go_Forward_Time = 1.3
Const_Desired_Color = Color.RED
ev3AdeptedFlineSpeed = 250

############################################################################
platformMap = [
  [pl.Platform(Color.RED),pl.Platform(Color.YELLOW),pl.Platform(Color.GREEN)],
  [pl.Platform(Color.GREEN),pl.Platform(Color.RED),pl.Platform(Color.BLUE)]
]
robotPosition = [0,0]
#####################################################################################
#разварачиваемся на 90 градусов
#directionTurn - выбор направления поворота  значение может быть 1 (направо) или -1 (налево)
def turn(directionTurn):
  print("turn:")
  print(directionTurn)
  gyroSensor.reset_angle(0)
  if(directionTurn == -1 or directionTurn == 1):
    motorRule(Const_turn_Speed *  directionTurn,-Const_turn_Speed *  directionTurn)
    while(True):
      if(abs(gyroSensor.angle()) >= Const_turn_Angle):
        motorStop()
        break
  else:
    motorRule(Const_turn_Speed,-Const_turn_Speed)
    while(True):
      if(abs(gyroSensor.angle()) >= Const_Razvorot_Angle):
        motorStop()
        break
  GoForward(Const_turn_Speed,Const_turn_Speed,0.5)
   
#захват кубика манипулятором
def grab():
  print("захватываем кубик")
  grabMotor.reset_angle(0)
  grabMotor.run(Const_Grab_Speed)
  while(True):
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
def crossroadGo(crossroadCounts):
  print("crossroadGo:")
  print(crossroadCounts)
  crossroad = 0
  blackLine = False
  print("едем по чёрной линии")
  while(True):
    reflectionLEFT = colorSensorLeft.reflection()
    reflectionRight = colorSensorRight.reflection()
    ev3AdeptedFline(reflectionLEFT,reflectionRight)
    
    if((reflectionLEFT < Const_Relection_Limit) & (reflectionRight < Const_Relection_Limit)):
      if(blackLine == False):
      
        crossroad = crossroad + 1
        if(crossroad == crossroadCounts):
          motorStop()
          return
      blackLine = True
    else:
      blackLine = False

#определяет путь от местоположение робота до нужной платформы
#Robot - координаты робота
#Platform - координаты платформы
def logic(Robot,Platform):
  print("logic:")
  print("рассчитываем путь")
  povorot1 = 0 
  povorot2 = 0
  print(Platform)
  horizontal = Platform[0] - Robot[0]

  robotWay = [["razovorot", 0 ],["crossroadGo",1] ]
  
  if(Robot[0]==Platform[0]):
    return [["razovorot", 0 ],["checkColor",0]]

  if(horizontal<0):
    povorot1 = -1
  else:
    povorot1 = 1
  if(Robot[1] == 0):
    povorot1 = povorot1 * -1
  
  if(horizontal>0):
    povorot2 = 1
  else:
    povorot2 = -1
  if(Platform[1]==0):
    povorot2 = povorot2 * -1
  
  robotWay.append(["turn",povorot1])
  robotWay.append(["crossroadGo",abs(horizontal)])
  robotWay.append(["turn",povorot2])
  robotWay.append(["checkColor",0])
  
  return robotWay

#вызывает последовательность методов соотвесвующие полученным командам
#robotWay - набор команд для проезда робота до нужной платформы
def perfomer(robotWay):
  print("perfomer:")
  print(robotWay)
  for way in robotWay:
    if(way[0] == "turn"):
      turn(way[1])
    elif(way[0] == "razovorot"):
      turn(0)
    elif(way[0] == "crossroadGo"):
      crossroadGo(way[1])
    elif(way[0] == "grab"):
      grab()
    elif(way[0] == "checkColor"):
      checkColor()

# смотрит цвет кубика и записывает его в переменную
def checkColor():
  print("чекаем цвет")
  color = None
  iteration = 0
  while(True):
    if(iteration % 2 == 0):
      reflectionLEFT = colorSensorLeft.reflection()
      reflectionRight = colorSensorRight.reflection()

      ev3AdeptedFline(reflectionLEFT,reflectionRight)
    color = filterColor()
    if(color != None):
      print("нашел цвет:")
      print(color)
      return color
    iteration = iteration + 1

#едем по чёрной линии
#reflectionLEFT - значение с датчика цвета
#reflectionRight - значение с датчика цвета
def fLine(reflectionLEFT,reflectionRight):
  if(reflectionLEFT < Const_Relection_Limit):
      if(reflectionRight < Const_Relection_Limit):
        motorRule(Const_Speed_Fline,Const_Speed_Fline)
      else:
        motorRule(-Const_Slow_Speed_Fline_Small,Const_Slow_Speed_Fline_Big)
  else:
      if(reflectionRight < Const_Relection_Limit):
        motorRule(Const_Slow_Speed_Fline_Big,-Const_Slow_Speed_Fline_Small)
      else:
        motorRule(Const_Speed_Fline,Const_Speed_Fline)

# метод для проезда вперёд на определёного времени
#left - скорость  левого мотора 
#right - скорость  правого мотора
#times - время на которое включиться оба мотора
def GoForward(left,right,times):
    print("проехать вперёд" + str(times)) 
    motorRule(left,right)
    oldTime = time.time()
    while(True):
        newTime = time.time()
        if(newTime - oldTime >= times):
          motorStop()
          return

#останавлевает оба мотора
def motorStop():
  print("выключаем оба мотора")
  leftMotor.stop()
  rightMotor.stop()

#метод для проезда до стартовой платформы
def start():
  print("едем до стартовой платформы")
  GoForward(Const_Go_Forward_Speed,Const_Go_Forward_Speed, Const_Go_Forward_Time)
  perfomer([["crossroadGo",1],["turn",-1],["checkColor",0]])
  
#ищет нужную платформу
def findColor(color):
  print("ищем нужную платформу")
  for x in range(0,3):
    for y in range(0,2):
      thisPlatform = platformMap[x][y]
      if(color == None):
        if(thisPlatform.status == 0):
            return [x,y]
      else:
        thisPlatform = platformMap[x][y]
        if(Const_Desired_Color == color):
          if(thisPlatform.status == -1 or thisPlatform.status == 0):
            return [x,y]

def pereborPlatform():
  print("перебираю гаражи")
  robotPosition = [0,0]
  for x in range(0,3): 
    for y in range(0,2):
      if(x != 0 or y != 0):
        #TODO
        newLogic = logic(robotPosition,[x,y])
        perfomer(newLogic)
        GoForward(-Const_Go_Forward_Speed,-Const_Go_Forward_Speed,)
        robotPosition = [x,y]
        if(filterColor()==Const_Desired_Color):
          return

def main():
  robotPosition = [0,0]
  start()
  if(filterColor()!=Const_Desired_Color):
    GoForward(-Const_Go_Forward_Speed,-Const_Go_Forward_Speed,Const_Go_Forward_Time)
    pereborPlatform()
  for x in range(0,6):
    colorPlatformPosition = findColor(filterColor())
    GoForward(20,20,0.4)#TODO
    grab()
    newLogic = logic(robotPosition,colorPlatformPosition)
    perfomer(newLogic)
    robotPosition = colorPlatformPosition
    ColorMap[colorPlatformPosition[0]][colorPlatformPosition[1]] = -1

def filterColor():
    color = colorSensorGruz.color()
    colorFilter = [Color.RED,Color.BLUE,Color.YELLOW,Color.GREEN]
    if(color in colorFilter):
      return(color)
    else:
      return(None)

def ev3AdepterMotorRule(angle,speed):
  
  angle = angle * 0.20
  if(angle>100):
    angle=100
  elif(angle<-100):
    angle = - 100
  factorAngleSpeed = (50 - abs(angle)) / 50
  if(angle > 0):
    motorRule(speed,speed * factorAngleSpeed)
  elif(angle < 0):
    motorRule(speed * factorAngleSpeed,speed)

def ev3AdeptedFline(reflectionLEFT,reflectionRight):
  ev3AdepterMotorRule(reflectionLEFT - reflectionRight,ev3AdeptedFlineSpeed)

main()