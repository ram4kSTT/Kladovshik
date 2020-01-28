#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 UltrasonicSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
# Новые импорты
import platform as pl
import time
# Инициализация моторов
leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)
grabMotor1 = Motor(Port.D)
grabMotor2 = Motor(Port.A)
# Инициализация датчиков
colorSensorGruz = ColorSensor(Port.S1)
colorSensorRight = ColorSensor(Port.S2)
colorSensorLeft = ColorSensor(Port.S3)
UltrasonicSensor = UltrasonicSensor(Port.S4)
# Константы
#Const_turn_Angle = 260
Const_turn_Angle = 195
Const_turn_Speed = 180
#Const_Razvorot_Angle = 460
Const_Razvorot_Angle = 390
Const_Grab_Speed = -125
Const_Grab_angle = 70
Const_Grab_angle2 = 275
Const_Normal_Distance = 60
Const_Go_Speed = 300
Const_Relection_Limit = 15
Const_Speed_Fline = 250
Const_Slow_Speed_Fline = 70
Const_MotorRule_Speed = 150
Const_checkColor_Speed = 50
Const_Go_Forward_Speed = 300
Const_Go_Forward_Time = 1.5
Const_Go_Forward_Turn_Time = 0.5
ev3AdeptedFlineSpeed = 250
# Начальный цвет
Const_Desired_Color = Color.RED
############################################################################
platformMap = [
  [pl.Platform(Color.RED),pl.Platform(Color.YELLOW),pl.Platform(Color.GREEN)],
  [pl.Platform(Color.GREEN),pl.Platform(Color.RED),pl.Platform(Color.BLUE)]
]
robotPosition = [0,0]
############################################################################
timeStart = 0
def log(*texts):
  print('TIME:['+str(time.time()-timeStart)+']')
  for text in texts:
    print(text)
  print('------------------------')


grabDirection = 1
#разварачиваемся на 90 градусов
#directionTurn - выбор напр+авления поворота  значение может быть 1 (направо) или -1 (налево)
def turn(directionTurn):
  log("Поворот (1 - право, -1 - лево, 0 - разворот):",directionTurn)
  rightMotor.reset_angle(0)
  if(directionTurn == 1 or directionTurn == -1):
    motorRule(Const_turn_Speed * directionTurn,-Const_turn_Speed * directionTurn)
    while(True):
      if(abs(rightMotor.angle()) >= Const_turn_Angle):
        motorStop()
        break
  else:
    rightMotor.reset_angle(0)
    motorRule(Const_turn_Speed,-Const_turn_Speed)
    while(True):
      if(abs(rightMotor.angle()) >= Const_Razvorot_Angle):
        motorStop()
        break
  GoForward(Const_Go_Forward_Speed,Const_Go_Forward_Speed,Const_Go_Forward_Turn_Time)
   # 1 первое действие 
#захват кубика манипулятором
def grab():
  global grabDirection
  log("Захватил кубик")
  capture()
  grabMotor2.reset_angle(0)
  grabMotor2.run(Const_Grab_Speed * grabDirection)
  grabDirection = grabDirection * -1
  while(True):
    if(abs(grabMotor2.angle()) >= Const_Grab_angle2 ):
        grabMotor2.stop()
        break
  capture()
  

isCapture = False
def capture():
  global isCapture
  grabMotor1.reset_angle(0)
  if(isCapture):
    grabMotor1.run(-Const_Grab_Speed)
  else:
    grabMotor1.run(Const_Grab_Speed)
  isCapture = not isCapture 
  while(True):
    if(abs(grabMotor1.angle()) >= Const_Grab_angle ):
        grabMotor1.stop()
        break
  
  
# метод для проезда вперёд на определёного времени
#left - скорость  левого мотора 
#right - скорость  правого мотора
#times - время на которое включиться оба мотора
def GoForward(left,right,times):
    log("Еду вперёд на заданное время",str(times)) 
    motorRule(left,right)
    oldTime = time.time()
    while(True):
        newTime = time.time()
        if(newTime - oldTime >= times):
          motorStop()
          return

#останавлевает оба мотора
def motorStop():
  log("Выключение моторов")
  leftMotor.stop()
  rightMotor.stop()

#езда по черной линии
#left - мощность левого мотора
#right - мощность правого мотора
def motorRule(left,right):
    leftMotor.run(left)
    rightMotor.run(right)

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

#езда по черной линии (реализанно так как в ev3)
#left - мощность левого мотора
#right - мощность правого мотора
def ev3AdepterMotorRule(angle,speed):
  angle = angle * 0.15
  if(angle>100):
    angle=100
  elif(angle<-100):
    angle = - 100
  factorAngleSpeed = (50 - abs(angle)) / 50
  if(angle > 0):
    motorRule(speed,speed * factorAngleSpeed)
  elif(angle < 0):
    motorRule(speed * factorAngleSpeed,speed)

#едем по чёрной линии (плавная реализация)
#reflectionLEFT - значение с датчика цвета
#reflectionRight - значение с датчика цвета
def ev3AdeptedFline(reflectionLEFT,reflectionRight):
  ev3AdepterMotorRule(reflectionLEFT - reflectionRight,ev3AdeptedflineSpeed)

#езда по черной линии
#crossroadCounts - кол-во перекрестков, которые необходимо проехать
def crossroadGo(crossroadCounts):
  log("Проезжаю заданное кол-во перекрестков:",crossroadCounts)
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
          return
      blackLine = True
    else:
      blackLine = False

def filterColor(sensor):
    color = sensor.color()
    distance = UltrasonicSensor.distance()
    colorFilter = [Color.RED,Color.BLUE,Color.YELLOW,Color.GREEN]
    if(distance < Const_Normal_Distance):
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

#определяет путь от местоположение робота до нужной платформы
#Robot - координаты робота
#Platform - координаты платформы
def logic(Robot,Platform):
  log("logic:")
  log("рассчитываем путь",Platform,Robot)
  povorot1 = 0 
  povorot2 = 0
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
def checkColor(colorPlatform):
  log("Еду вперед и жду платформу или цвет:",colorPlatform)
  if(isCapture):
    capture()
  color = None
  iteration = 0
  while(True):
    distance = UltrasonicSensor.distance()
    reflectionLEFT = colorSensorLeft.reflection()
    reflectionRight = colorSensorRight.reflection()
    if(iteration % 2 == 0):
      if(distance > Const_Normal_Distance):
        fLine(reflectionLEFT,reflectionRight)
      else:
        motorRule(Const_Slow_Speed_Fline,Const_Slow_Speed_Fline)
    if(colorPlatform != None):
      if(colorPlatform == filterColor(colorSensorLeft)):
        return None
    else:
      color = filterColor(colorSensorGruz)
      if(color != None):
        log("Нашел кубик цвета:",color)
        return color
    iteration = iteration + 1

#вызывает последовательность методов соотвесвующие полученным командам
#robotWay - набор команд для проезда робота до нужной платформы
def perfomer(robotWay):
  log("Метод исполнитель(perfomer)","Исполняю:",robotWay)
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
  log("Еду до стартовой платформы")
  GoForward(Const_Go_Forward_Speed,Const_Go_Forward_Speed, Const_Go_Forward_Time)
  perfomer([["crossroadGo",1],["turn",-1]])
  
#ищет нужную платформу
def findColor(color):
  log("Ищем нужную платформу",'цвет:',str(color))
  for x in range(0,3):
    for y in range(0,2):
      distance = UltrasonicSensor.distance()
      thisPlatform = platformMap[y][x]
      if(color == None):
        if(thisPlatform.status == 0):
            return [y,x]
      else:
        if(thisPlatform.color == color):
          if(thisPlatform.status == -1 or thisPlatform.status == 0):
            return [y,x]
  log("ERROR: ничего не нашел")

# Перебираем платформы пока не найдем нужный цвет
def pereborPlatform():
  global robotPosition
  log("Перебираю гаражи в поисках начального цвета")
  for x in range(0,3): 
    for y in range(0,2):
      if(x != 0 or y != 0):
        #TODO
        newLogic = logic(robotPosition,[y,x])
        perfomer(newLogic)
        color = checkColor(None)
        robotPosition = [y,x]
        if(color==Const_Desired_Color):
          log('Нашел нужный цвет',color)
          GoForward(Const_Go_Forward_Speed,Const_Go_Forward_Speed,0.2)
          
          return robotPosition
        GoForward(-Const_Go_Forward_Speed,-Const_Go_Forward_Speed,Const_Go_Forward_Time/2)
        

def main():
  global timeStart
  timeStart = time.time()
  
  cubeStorage = False
  global robotPosition
  capture()
  start()
  color = checkColor(None)

  

  if(filterColor(colorSensorGruz)!=Const_Desired_Color):
    GoForward(-Const_Go_Forward_Speed,-Const_Go_Forward_Speed,Const_Go_Forward_Time/2)
    pereborPlatform()
    platformMap[robotPosition[0]][robotPosition[1]].status= -1
    cubeStorage = True

  for x in range(0,6):
    colorPlatformPosition = findColor(filterColor(colorSensorGruz))
    GoForward(20,20,0.2)#TODO константы!
    grab()
    GoForward(-Const_Go_Forward_Speed,-Const_Go_Forward_Speed,Const_Go_Forward_Time/2)
    capture()

    newLogic = logic(robotPosition,colorPlatformPosition)
    perfomer(newLogic)
    robotPosition = colorPlatformPosition
    #Если мы знаем, что едем нга пустую платформу, то вызываем checkColor с параметром не NONE
    if(platformMap[colorPlatformPosition[0]][colorPlatformPosition[1]].status == -1):
      checkColor(platformMap[colorPlatformPosition[0]][colorPlatformPosition[1]].color)
      grab()
      nextColorPlatformPosition = findColor(None)
      newLogic = logic(robotPosition,colorPlatformPosition)
      perfomer(newLogic)
      robotPosition = nextColorPlatformPosition
    #Если вернет None то ищем другую платформу для начала
    else:
      checkColor(None)
     
    if(cubeStorage):
      platformMap[robotPosition[0]][robotPosition[1]].status = 1
    else:
      platformMap[robotPosition[0]][robotPosition[1]].status = -1
    cubeStorage = 1

main()