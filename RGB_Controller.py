from machine import Pin, PWM
from time import time, sleep
from random import randint


class RGB_Controller:

    def __init__(self, red_pin_num=17, green_pin_num=16, blue_pin_num=19, freq=500):
        self.red = PWM(Pin(red_pin_num))
        self.green = PWM(Pin(green_pin_num))
        self.blue = PWM(Pin(blue_pin_num))

        self.red.freq(freq)
        self.green.freq(freq)
        self.blue.freq(freq)

        self.red.duty_u16(0)
        self.green.duty_u16(0)
        self.blue.duty_u16(0)

    def set_freq(self, freq):
        self.red.freq(freq)
        self.green.freq(freq)
        self.blue.freq(freq)

    def set_rgb_u16(self, red_u16, green_u16, blue_u16):
        """
        Sets the R, G and B diodes to specified values in range of 0 to 65535 (16-bit value).
        Prints values to terminal.
        """
        self.red.duty_u16(red_u16)
        self.green.duty_u16(green_u16)
        self.blue.duty_u16(blue_u16)

        print(f"R: {red_u16}, G: {green_u16}, B: {blue_u16}")

    def set_rgb_percent(self, red_percent, green_percent, blue_percent):
        """
        Sets the R, G and B diodes to specified values in range of 0 to 100.
        Prints values to terminal.
        """
        U_16 = 2**16 - 1
        self.red.duty_u16(int(red_percent * U_16))
        self.green.duty_u16(int(green_percent * U_16))
        self.blue.duty_u16(int(blue_percent * U_16))

        print(f"R: {red_percent}%, G: {green_percent}%, B: {blue_percent}%")

    def random_rgb(self):
        """
        Randomizes and sets R, G, and B diodes within the range of 0 to 65535.
        """
        rand_red = randint(0, 65535)
        rand_green = randint(0, 65535)
        rand_blue = randint(0, 65535)

        self.set_rgb_u16(rand_red, rand_green, rand_blue)

    def effect_randomize(self, duration_seconds, interval_seconds):
        """
        Randomizes R, G, and B diodes within the range of 0 to 65535.

        Args:
        duration (int): The total duration for which to strobe the diodes (in seconds).
        interval (float): The interval between each strobe (in seconds).

        Returns:
        None
        """
        start_time = time()
        while time() - start_time < duration_seconds:
            self.random_rgb()

            sleep(interval_seconds)
