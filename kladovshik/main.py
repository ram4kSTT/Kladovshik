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
grabMotor = Motor(Port.A)
colorSensorGruz = ColorSensor(Port.S1)
colorSensorRight = ColorSensor(Port.S2)
colorSensorLeft = ColorSensor(Port.S3)
Const_turn_Angle = 170
Const_turn_Speed = 50
Const_Razvorot_Angle = 330
Const_Razvorot_Speed = 50
Const_Grab_Speed = 200
Const_Grab_angle = 150
Const_Go_Speed = 200
Const_Relection_Limit = 20
Const_Speed_Fline = 170
Const_Slow_Speed_Fline = 50
Const_MotorRule_Speed = 150
Const_checkColor_Speed = 50
robotPosition = [0,0]
actualColor = 0


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
  motorRule(Const_turn_Speed *  directionTurn,-Const_turn_Speed *  directionTurn)
  while(True):
      angle = abs(leftMotor.angle())
      if(angle >= Const_turn_Angle):
          motorStop()
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
    elif(way[0] == "crossroadGo"):
      crossroadGo(way[1])
    elif(way[0] == "grab"):
      grab()
    elif(way[0] == "checkColor"):
      checkColor()


# смотрит цвет кубика и записывает его в переменную
def checkColor():
  print("чекаем цвет")
  actualColor = colorSensorGruz.color()
  while(actualColor == None):
    reflectionLEFT = colorSensorLeft.reflection()
    reflectionRight = colorSensorRight.reflection()
    fLine
      
    return
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



def motorStop():
  leftMotor.stop()
  rightMotor.stop()

        


def start():
  crossroadGo(1)
  turn(-1)
  checkColor()
  


start()
perfomer(logic(robotPosition,[2,1]))