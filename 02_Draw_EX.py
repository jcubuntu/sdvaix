import image
import lcd
import time

lcd.init(type=2, freq=20000000, color=lcd.BLACK)

img = image.Image(size=(240,240))
#img.draw_circle(120,120,100,color=(200,200,0),fill=True)
#img.draw_cross(120,120,color=(0,0,0),size=100,thickness=2)
for x in range(0,240,10):
    img.draw_line(0,x,x+10,240,color=(255,255,255))
    time.sleep(0.2)
    lcd.display(img)
