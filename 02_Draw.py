import image
import lcd

lcd.init(type=2, freq=20000000, color=lcd.BLACK)

img = image.Image(size=(240,240))
img.draw_circle(120,120,100,color=(200,200,0),fill=True)
img.draw_cross(120,120,color=(0,0,0),size=100,thickness=2)

lcd.display(img)
