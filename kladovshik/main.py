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
Const_Grab_Speed = -125
Const_Grab_angle = 180
Const_Go_Speed = 200
Const_Relection_Limit = 15
Const_Speed_Fline = 250
Const_Slow_Speed_Fline_Big= 150
Const_Slow_Speed_Fline_Small = -50
Const_MotorRule_Speed = 150
Const_checkColor_Speed = 50
Const_Go_Forward_Speed = 300
Const_Go_Forward_Time = 1.5
Const_Desired_Color = 5
ev3AdeptedFlineSpeed = 250

checkedColor = Color.BLACK
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
    if(colorSensorLeft.color = Color.WHITE):
      
  GoForward(Const_turn_Speed,Const_turn_Speed,0.5)
   
#захват кубика манипулятором
def grab():
  print("захватываем кубик")
  grabMotor.reset_angle(0)
  grabMotor.run(Const_Grab_Speed)
  while(True):
    if(abs(grabMotor.angle()) >= Const_Grab_angle ):
        print("кубик")
        grabMotor.stop()
        return


#езда по черной линии
#left - мощность левого мотора
#right - мощность правого мотора
def motorRule(left,right):
    leftMotor.run(left)
    rightMotor.run(right)

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
  print(Robot)
  horizontal = Platform[1] - Robot[1]

  robotWay = [["razovorot", 0 ],["crossroadGo",1] ]
  
  if(Robot[1]==Platform[1]):
    return [["razovorot", 0 ],["checkColor",0]]

  if(horizontal<0):
    povorot1 = -1
  else:
    povorot1 = 1
  if(Robot[0] == 0):
    povorot1 = povorot1 * -1
  
  if(horizontal>0):
    povorot2 = 1
  else:
    povorot2 = -1
  if(Platform[0]==0):
    povorot2 = povorot2 * -1
  
  robotWay.append(["turn",povorot1])
  robotWay.append(["crossroadGo",abs(horizontal)])
  robotWay.append(["turn",povorot2])
  
  return robotWay


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

#метод для проезда до стартовой платформы
def start():
  print("едем до стартовой платформы")
  GoForward(Const_Go_Forward_Speed,Const_Go_Forward_Speed, Const_Go_Forward_Time)
  perfomer([["crossroadGo",1],["turn",-1]])
  
#ищет нужную платформу
def findColor(color):
  print("ищем нужную платформу")
  print('цвет:'+str(color))
  for x in range(0,3):
    for y in range(0,2):
      thisPlatform = platformMap[y][x]
      if(color == None):
        if(thisPlatform.status == 0):
            return [y,x]
      else:
        if(thisPlatform.color == color):
          if(thisPlatform.status == -1 or thisPlatform.status == 0):
            return [y,x]
  print("ничего не нашел")

def pereborPlatform(robotPosition):
  print("перебираю гаражи")
  for x in range(0,3): 
    for y in range(0,2):
      if(x != 0 or y != 0):
        #TODO
        newLogic = logic(robotPosition,[y,x])
        perfomer(newLogic)
        color = checkColor()
        robotPosition = [y,x]
        if(color==Const_Desired_Color):
          print('Нашел нужный цвет')
          print(color)
          return robotPosition
        GoForward(-Const_Go_Forward_Speed,-Const_Go_Forward_Speed,Const_Go_Forward_Time/2)
        

def main():
  cubeStorage = False
  robotPosition = [0,0]
  start()
  color = checkColor()
  if(filterColor()!=Const_Desired_Color):
    GoForward(-Const_Go_Forward_Speed,-Const_Go_Forward_Speed,Const_Go_Forward_Time/2)
    robotPosition = pereborPlatform(robotPosition)
    platformMap[robotPosition[0]][robotPosition[1]].status= -1
    cubeStorage = True
  print('нашел нужный цвет!')
  for x in range(0,6):
    colorPlatformPosition = findColor(filterColor())
    GoForward(20,20,0.2)#TODO
    grab()
    GoForward(20,20,0.-0.2)
    newLogic = logic(robotPosition,colorPlatformPosition)
    perfomer(newLogic)
    color = checkColor()
    robotPosition = colorPlatformPosition
    if(cubeStorage):
      platformMap[robotPosition[0]][robotPosition[1]].status = 1
    else:
      platformMap[robotPosition[0]][robotPosition[1]].status = -1
    cubeStorage = 1

def filterColor():
    color = colorSensorGruz.color()
    colorFilter = [Color.RED,Color.BLUE,Color.YELLOW,Color.GREEN]
    if(color == Color.BROWN):
      color = Color.YELLOW
    if(color == Color.GREEN):
      if(colorSensorGruz.rgb()[1] < colorSensorGruz.rgb()[2]):
        color = Color.BLUE
      else:
        color = color
    if(color in colorFilter):
      return(color)
    else:
      return(None)

main()