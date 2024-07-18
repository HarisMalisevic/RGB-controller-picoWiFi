from machine import Pin, PWM
from time import time, sleep
from random import randint

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

def set_rgb(red_u16, green_u16, blue_u16):
    red.duty_u16(red_u16)
    green.duty_u16(green_u16)
    blue.duty_u16(blue_u16)



def strobe_diodes(duration_seconds, interval_seconds):
    global red, green, blue
    """
    Strobes R, G, and B diodes within the range of 0 to 65535.

    Args:
    duration (int): The total duration for which to strobe the diodes (in seconds).
    interval (float): The interval between each strobe (in seconds).

    Returns:
    None
    """
    start_time = time()
    while time() - start_time < duration_seconds:
        rand_red = randint(0, 65535)
        rand_green = randint(0, 65535)
        rand_blue = randint(0, 65535)

        print(f"R: {rand_red}, G: {rand_green}, B: {rand_blue}")

        set_rgb(rand_red, rand_green, rand_blue)
        
        # Replace the print statement with actual code to set the diode values
        # e.g., set_diode_values(r_value, g_value, b_value)

        sleep(interval_seconds)

# Example usage:
strobe_diodes(2, 0.5)
set_rgb(U_16, 0, U_16)

while True:
    pass
