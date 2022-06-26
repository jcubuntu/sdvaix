import lcd, time, sensor, image
from machine import I2C
from board import board_info
from Maix import GPIO

lcd.init()
lcd.rotation(2)
sensor.reset(dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(30)

i2c = I2C(I2C.I2C0, freq=100000, scl=30, sda=32)
color_threshold = (33, 72, 20, 51, -2, 44)

def motorControl(speedLeft,speedRight):
    i2c.writeto(0x12,bytes([int(127+speedLeft),int(127+speedRight),int(1)]))

while True:
        img=sensor.snapshot()
        blobs = img.find_blobs([color_threshold],area_threshold=500, pixels_threshold=500)
        if blobs:
            for b in blobs:
                if b.cx() < 120 :
                    motorControl(-20,20)
                elif b.cx() > 200 :
                    motorControl(20,-20)
                else :
                    motorControl(0,0)
                tmp=img.draw_rectangle(b[0:4],thickness=2,color=(0,0,255))
                tmp=img.draw_cross(b[5], b[6],thickness=4,color=(0,255,0),size=8)
                c=img.get_pixel(b[5], b[6])
        else :
            motorControl(0,0)

        lcd.display(img)
