from machine import I2C
import time

i2c = I2C(I2C.I2C0, freq=100000, scl=35, sda=34)

while True:
    controlData = i2c.readfrom(0x12, 3)
    print(controlData[0], ",", controlData[1], ",", controlData[2])
    time.sleep_ms(100)
