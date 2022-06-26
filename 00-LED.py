from fpioa_manager import fm
from Maix import GPIO

fm.register(12, fm.fpioa.GPIO0)
led_r=GPIO(GPIO.GPIO0, GPIO.OUT)
led_r.value(0)
