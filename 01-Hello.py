import Maix
import image
import lcd

lcd.init(type=2, freq=20000000, color=lcd.BLACK)

img = image.Image(size=(240,240))
img.draw_string(50,70,"Hello World",color=(255,0,255),scale=2)

lcd.display(img)
