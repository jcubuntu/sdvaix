import sensor, image, time, lcd

lcd.init(freq=20000000)

sensor.reset(dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(40)


while(True):
    img = sensor.snapshot()
    lcd.display(img)
