from RGB_Controller import RGB_Controller

rgb_controller = RGB_Controller(17, 16, 19)

# Example usage:
rgb_controller.randomize(2, 0.1)
rgb_controller.set_rgb(0, 0, 65535)

while True:
    pass
