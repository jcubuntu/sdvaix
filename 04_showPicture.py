import lcd
import image

print("init")
lcd.init(freq=20000000)
print("init ok")

path="/sd/demo/logo.jpg"
print("read image")
img_read = image.Image(path)
lcd.display(img_read)
print("ok")
