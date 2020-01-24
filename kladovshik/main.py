#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
import time
# Write your program here


leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)
grabMotor = Motor(Port.D)

colorSensorGruz = ColorSensor(Port.S1)
colorSensorRight = ColorSensor(Port.S2)
colorSensorLeft = ColorSensor(Port.S3)

Const_turn_Angle = 200
Const_turn_Speed = 50
Const_Razvorot_Angle = 400
Const_Razvorot_Speed = 50
Const_Grab_Speed = 50
Const_Grab_angle = 140
Const_Go_Speed = 200
Const_Relection_Limit = 8
Const_Speed_Fline = 170
Const_Slow_Speed_Fline = 50
Const_MotorRule_Speed = 150
Const_checkColor_Speed = 50
Const_Go_Forward_Speed = 300
Const_Go_Forward_Time = 0.75
Const_Desired_Color = Color.RED

##################################################################################
ColorMap = [
    [Color.RED,Color.YELLOW,Color.GREEN],
    [Color.GREEN,Color.RED,Color.BLUE]
    ]
robotPosition = [0,0]
#####################################################################################
#разварачиваемся на 90 градусов
#directionTurn - выбор направления поворота  значение может быть 1 (направо) или -1 (налево)
def turn(directionTurn):
  print("turn:")
  print(directionTurn)
  leftMotor.reset_angle(0)
  motorRule(Const_turn_Speed *  directionTurn,-Const_turn_Speed *  directionTurn)
  while(True):
      angle = abs(leftMotor.angle())
      if(angle >= Const_turn_Angle):
          motorStop()
          GoForward(Const_Go_Forward_Speed,Const_Go_Forward_Speed,Const_Go_Forward_Time)
          break

#разварачиваемся на 180 градусов
def razovorot():
  print("разворачиваемся")
  leftMotor.reset_angle(0)
  motorRule(Const_Razvorot_Speed,-Const_Razvorot_Speed)
  while(True):
      angle = abs(leftMotor.angle())
      if(angle >= Const_Razvorot_Angle):
          motorStop()
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
def crossroadGo(crossroadCounts):
  print("crossroadGo:")
  print(crossroadCounts)
  crossroad = 0
  blackLine = False
  print("едем по чёрной линии")
  while(True):
    reflectionLEFT = colorSensorLeft.reflection()
    reflectionRight = colorSensorRight.reflection()
    fLine(reflectionLEFT,reflectionRight)
    
    if((reflectionLEFT < Const_Relection_Limit) & (reflectionRight < Const_Relection_Limit)):
      if(blackLine == False):
      
        crossroad = crossroad + 1
        if(crossroad == crossroadCounts):
          motorStop()
          break
      blackLine = True
    else:
      blackLine = False
    color = colorSensorGruz.color()

#определяет путь от местоположение робота до нужной платформы
#Robot - координаты робота
#Platform - координаты платформы
def logic(Robot,Platform):
  print("logic:")
  print("рассчитываем путь")
  povorot1 = 0 
  povorot2 = 0
  horizontal = Platform[0] - Robot[0]

  robotWay = [["razovorot", 0 ],["crossroadGo",1] ]
  
  if(Robot[0]==Platform[0]):
    return [["razovorot", 0 ],["crossroadGo",1],["checkColor",0]]

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
      razovorot()
    elif(way[0] == "crossroadGo"):
      crossroadGo(way[1])
    elif(way[0] == "grab"):
      grab()
    elif(way[0] == "checkColor"):
      checkColor()

# смотрит цвет кубика и записывает его в переменную
def checkColor():
  print("чекаем цвет")
  color = colorSensorGruz.color()
  while (colorSensorGruz.color() == None):
    reflectionLEFT = colorSensorLeft.reflection()
    reflectionRight = colorSensorRight.reflection()
    fLine(reflectionLEFT,reflectionRight)
  print(colorSensorGruz.color())
  filterColor(color)
  return colorSensorGruz.color()

#едем по чёрной линии
#reflectionLEFT - значение с датчика цвета
#reflectionRight - значение с датчика цвета
def fLine(reflectionLEFT,reflectionRight):
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

# метод для проезда вперёд на определёного времени
#left - скорость  левого мотора 
#right - скорость  правого мотора
#times - время на которое включиться оба мотора
def GoForward(left,right,times):
    print("проехать вперёд" + str(times)) 
    motorRule(Const_Go_Forward_Speed,Const_Go_Forward_Speed)
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
  foundColor = ColorMap[0].index(color)
  if(Const_Desired_Color == foundColor):
    if(foundColor!=-1):
      return [foundColor,0]
    foundColor = ColorMap[1].index(color)
    if(foundColor!=-1):
      return [foundColor,1]
  else:
    razovorot()
    crossroadGo(1)

    checkColor()

def pereborPlatform():
  print("перебираю гаражи")
  robotPosition = [0,0]
  for x in range(0,3): 
    for y in range(0,2):
      if(x != 0 or y != 0):
        #TODO
        newLogic = logic(robotPosition,[x,y])
        perfomer(newLogic)
        robotPosition = [x,y]
        if(colorSensorGruz.color()==Const_Desired_Color):
          return

def main():
  robotPosition = [0,0]
  start()
  if(colorSensorGruz.color()!=Const_Desired_Color):
    pereborPlatform()
  for x in range(0,6):
    colorPlatformPosition = findColor(colorSensorGruz.color())
    GoForward(20,20,0.4)#TODO
    grab()
    newLogic = logic(colorPlatformPosition)
    perfomer(newLogic)
    robotPosition = colorPlatformPosition
    ColorMap[colorPlatformPosition[0]][colorPlatformPosition[1]] = -1



def filterColor(color):
  # colorFilter = [Color.RED,Color.BLUE,Color.YELLOW,Color.GREEN]
  # if(colorFilter.index(color) == -1):
    # return(None)
  # else:
  return(color)

start()