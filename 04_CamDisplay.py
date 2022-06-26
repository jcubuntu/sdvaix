import sensor, image, time, lcd

lcd.init()
lcd.rotation(2)

sensor.reset(dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(40)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    lcd.display(img)
    print(clock.fps())
