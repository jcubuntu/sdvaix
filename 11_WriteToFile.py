from machine import I2C
import lcd, time, os, image

lcd.init(type=2, freq=20000000, color=lcd.BLACK)
i2c = I2C(I2C.I2C0, freq=100000, scl=35, sda=34)

img_co_l = 0
img_co_f = 0
img_co_r = 0

thisTime = lastTime = time.ticks_ms()

f = open('/sd/dataset.csv', 'a+')
img = image.Image(size=(240,240))

while True:
    thisTime = time.ticks_ms()
    if (thisTime - lastTime) >= 50 :
        lastTime = thisTime
        readData = i2c.readfrom(0x12, 3)
        if (int(readData[2]) == 4) and (int(readData[0]) > 135) :
            if readData[1] < 85:
                img_co_l = img_co_l+1
            elif readData[1] < 170:
                img_co_f = img_co_f+1
            else:
                img_co_r = img_co_r+1
            f.write(str(int(readData[0]))+","+str(int(readData[1]))+"\n")
            f.flush()
        img = image.Image(size=(240,240))
        img.draw_string(50, 0,  "L = "+str(img_co_l), scale=2)
        img.draw_string(50, 20, "F = "+str(img_co_f), scale=2)
        img.draw_string(50, 40, "R = "+str(img_co_r), scale=2)
        lcd.display(img)
