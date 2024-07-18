from machine import Pin, PWM

red = PWM(Pin(17))
green = PWM(Pin(16))
blue = PWM(Pin(19))

red.freq(500)
green.freq(500)
blue.freq(500)

U_16 = 2**16 - 1

red.duty_u16(0)
green.duty_u16(0)
blue.duty_u16(0)

while True:
    pass
