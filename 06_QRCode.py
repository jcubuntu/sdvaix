import sensor, image, lcd, time

lcd.init()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)
sensor.skip_frames(30)

while True:
    img=sensor.snapshot()
    qr = img.find_qrcodes()
    if len(qr) > 0:
        img.draw_string(2,2,"QR:" + qr[0].payload(), color=(0,255,0), scale=2)
        img.draw_rectangle(qr[0].rect(),color=(0,0,255),thickness=2)
    lcd.display(img)

