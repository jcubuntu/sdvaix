import sensor, image, lcd, time
from machine import I2C
from fpioa_manager import fm
from Maix import GPIO

i2c = I2C(I2C.I2C0, freq=100000, scl=30, sda=32)

lcd.init()
lcd.rotation(2)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(30)

def motorControl(speedL,speedR):
    i2c.writeto(0x12,bytes([int(127+speedL),int(127+speedR),int(1)]))

color_threshold = (76, 96, -18, 51, 31, 75)

while True:
    img=sensor.snapshot()
    blobs = img.find_blobs([color_threshold],area_threshold=200, pixels_threshold=200)

    if blobs:
        print(blobs[0].cx())
        if (blobs[0].cx() < 110):
            motorControl(-25,25)
        elif (blobs[0].cx() > 210) :
            motorControl(25,-25)
        else :
            motorControl(0,-0)
    else :
        motorControl(0,0)
        #for b in blobs:
            #tmp=img.draw_rectangle(b[0:4],thickness=2,color=(0,0,255))
            #tmp=img.draw_cross(b[5], b[6],thickness=4,color=(0,255,0),size=8)
            #c=img.get_pixel(b[5], b[6])
    lcd.display(img)
