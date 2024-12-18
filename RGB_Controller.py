from machine import Pin, PWM
from time import time, sleep
from random import randint


class RGB_Controller:

    U_16 = 2**16 - 1

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

    def set_pwm_freq(self, freq):
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

        print(
            f"R: {self.red.duty_u16()}, G: {self.green.duty_u16()}, B: {self.blue.duty_u16()}"
        )

    def set_red_u16(self, red_u16):
        """
        Sets the Red diode to specified value in range of 0 to 65535 (16-bit value).
        Prints values to terminal.
        """
        self.red.duty_u16(red_u16)

        print(
            f"R: {self.red.duty_u16()}, G: {self.green.duty_u16()}, B: {self.blue.duty_u16()}"
        )

    def set_green_u16(self, green_u16):
        """
        Sets the Green diode to specified value in range of 0 to 65535 (16-bit value).
        Prints values to terminal.
        """

        self.green.duty_u16(green_u16)

        print(
            f"R: {self.red.duty_u16()}, G: {self.green.duty_u16()}, B: {self.blue.duty_u16()}"
        )

    def set_blue_u16(self, blue_u16):
        """
        Sets the Blue diode to specified value in range of 0 to 65535 (16-bit value).
        Prints values to terminal.
        """
        self.blue.duty_u16(blue_u16)

        print(
            f"R: {self.red.duty_u16()}, G: {self.green.duty_u16()}, B: {self.blue.duty_u16()}"
        )

    def random_rgb(self):
        """
        Randomizes and sets R, G, and B diodes within the range of 0 to 65535.
        """
        rand_red = randint(0, self.U_16)
        rand_green = randint(0, self.U_16)
        rand_blue = randint(0, self.U_16)

        self.set_rgb_u16(rand_red, rand_green, rand_blue)

    class Effects:
        @staticmethod
        def randomize(controller, duration_seconds, interval_seconds):
            """
            Randomizes R, G, and B diodes within the range of 0 to 65535.

            Args:
            controller (RGB_Controller): The RGB controller object.
            duration_seconds (int): The total duration for which to strobe the diodes (in seconds).
            interval_seconds (float): The interval between each strobe (in seconds).

            Returns:
            None
            """
            start_time = time()
            while time() - start_time < duration_seconds:
                controller.random_rgb()
                sleep(interval_seconds)
