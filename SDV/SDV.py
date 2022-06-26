import sensor, image, time, lcd
import math
import utime
from machine import I2C
from fpioa_manager import fm
from Maix import GPIO


COLOR_THRESHOLDS =[(94, 100, -27, 3, 27, 127)]
GRAYSCALE_THRESHOLDS = [(240, 255)] # White Line.
COLOR_HIGH_LIGHT_THRESHOLDS = [(80, 100, -10, 10, -10, 10)]
GRAYSCALE_HIGH_LIGHT_THRESHOLDS = [(250, 255)]
BINARY_VIEW = False # Helps debugging but costs FPS if on.
DO_NOTHING = False # Just capture frames...
FRAME_SIZE = sensor.QQVGA # Frame size.
FRAME_REGION = 0.75 # Percentage of the image from the bottom (0 - 1.0).
FRAME_WIDE = 1.0 # Percentage of the frame width.

AREA_THRESHOLD = 0 # Raise to filter out false detections.
PIXELS_THRESHOLD = 40 # Raise to filter out false detections.
MAG_THRESHOLD = 4 # Raise to filter out false detections.
MIXING_RATE = 0.9 # Percentage of a new line detection to mix into current steering.


lcd.init()
lcd.rotation(2)
sensor.reset(dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.set_auto_gain(False,200)
sensor.run(1)
sensor.skip_frames(40)
i2c = I2C(I2C.I2C0, freq=100000, scl=30, sda=32)

clock = time.clock()
old_cx_normal = None
img = {}
img2 = {}
line = {}

def laneValue(line, img):
    global old_cx_normal
    cy = img.height() / 2
    cx = (line.rho() - (cy * math.sin(math.radians(line.theta())))) / math.cos(math.radians(line.theta()))
    cx_middle = cx - (img.width() / 2)
    cx_normal = cx_middle / (img.width() / 2)
    if old_cx_normal != None: old_cx_normal = (cx_normal * MIXING_RATE) + (old_cx_normal * (1.0 - MIXING_RATE))
    else: old_cx_normal = cx_normal
    return old_cx_normal

def readCam():
    global img
    global img2
    img = sensor.snapshot()
    img2 = img.copy()

def readLane():
    global img
    global img2
    global line
    readCam()
    img.binary(COLOR_HIGH_LIGHT_THRESHOLDS , zero = True)
    img.histeq()
    line = img.get_regression(COLOR_THRESHOLDS, \
        area_threshold = AREA_THRESHOLD, pixels_threshold = PIXELS_THRESHOLD, \
        robust = True)
        
def motorControl(speedL,speedR,Active):
    i2c.writeto(0x12,bytes([int(127+speedL),int(127+speedR),int(1)]))

baseSpeed = 27 #27
error = 0
last_error = 0
pidValue = 0
leftSpeed = 0
rightSpeed = 0

Kp = 14
Kd = 10

while True:
    readLane()
    if line and (line.magnitude() >= MAG_THRESHOLD):
        #img.draw_line(line.line(), thickness=2,color = (127, 127, 255) if COLOR_LINE_FOLLOWING else 127)
        img2.draw_line(line.line(), color = (127, 127, 255),thickness=3)
        error = laneValue(line, img)
        pidValue = (Kp * error) + (Kd * (error - last_error))
        last_error = error
        if pidValue <= (-baseSpeed) : pidValue = (-baseSpeed)
        if pidValue >= baseSpeed : pidValue = baseSpeed
        leftSpeed = 127 + (int(baseSpeed + pidValue))
        rightSpeed = 127 + (int(baseSpeed - pidValue))

    i2c.writeto(0x12,bytes([int(leftSpeed),int(rightSpeed)]))    
    print(error)
