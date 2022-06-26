import sensor, lcd, image

lcd.init()
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(40)

path = "/flash/image.jpg"
img = sensor.snapshot()
lcd.display(img)
print("save image")
img.save(path)
