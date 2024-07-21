import network
import simple
from machine import Timer
from RGB_Controller import RGB_Controller

U_16 = 2**16 - 1

# RGB Controller Setup
RGB_CONTROLLER = RGB_Controller(17, 16, 19)

# WiFi configuration
WIFI_SSID = "Malisevic"
WIFI_PASSWORD = "Ari_bjelov"

# Connecting to WiFi
print("Connecting to WiFi: ", WIFI_SSID)
WIFI = network.WLAN(network.STA_IF)
WIFI.active(True)
WIFI.config(pm=0xA11140)
WIFI.connect(WIFI_SSID, WIFI_PASSWORD)

while not WIFI.isconnected():
    pass

print("Connected to network!")
print("IP address:", WIFI.ifconfig()[0])


# Function to reconnect to WiFi
def reconnect_wifi():
    print("Reconnecting to WiFi...")
    WIFI.disconnect()
    WIFI.connect(WIFI_SSID, WIFI_PASSWORD)
    while not WIFI.isconnected():
        pass
    print("Connected to network!")
    print("IP address:", WIFI.ifconfig()[0])


# Reconnect to WiFi if the connection broke
def check_wifi_connection(timer):
    if not WIFI.isconnected():
        reconnect_wifi()


# Check WiFi connection every 1 minute
CHECK_CONNECTION_TIMER = Timer(
    period=60000, mode=Timer.PERIODIC, callback=check_wifi_connection
)

# MQTT Configuration

# MQTT Configuration
MQTT_SERVER =  "192.168.1.12" #"broker.hivemq.com"
MQTT_CLIENT_NAME = "RGB-Controller"

MQTT_TOPIC_RED = b"RGB-Controller/red"
MQTT_TOPIC_GREEN = b"RGB-Controller/green"
MQTT_TOPIC_BLUE = b"RGB-Controller/blue"
MQTT_TOPIC_RGB = b"RGB-Controller/RGB_set"


def parse_rgb_string(rgb_bytes):
    # Decode the bytes object to a string
    rgb_string = rgb_bytes.decode("utf-8")

    # Extract the numeric values from the string
    rgb_values = rgb_string.split("(")[1].split(")")[0].split(",")

    # Convert the extracted values to integers in ragne [0, 255]
    r, g, b = [int(value.strip()) for value in rgb_values]

    # Scale the values to a range of 0 to 65535 (U_16)
    r_scaled = (r / 255) * U_16
    g_scaled = (g / 255) * U_16
    b_scaled = (b / 255) * U_16

    return int(r_scaled), int(g_scaled), int(b_scaled)


# Example usage
rgb_string = b"rgb(86, 255, 0)"
r, g, b = parse_rgb_string(rgb_string)
print(r, g, b)


# MQTT Filtering recieved messages
def custom_dispatcher(topic, msg):
    global red_percent, green_percent, blue_percent

    if topic == MQTT_TOPIC_RED:
        r = int(float(msg))
        RGB_CONTROLLER.set_red_u16(r)

    elif topic == MQTT_TOPIC_GREEN:
        g = int(float(msg))
        RGB_CONTROLLER.set_green_u16(g)

    elif topic == MQTT_TOPIC_BLUE:
        b = int(float(msg))
        RGB_CONTROLLER.set_blue_u16(b)

    elif topic == MQTT_TOPIC_RGB:
        r, g, b = parse_rgb_string(msg)
        RGB_CONTROLLER.set_rgb_u16(r, g, b)


# MQTT Connecting to broker
CLIENT = simple.MQTTClient(client_id=MQTT_CLIENT_NAME, server=MQTT_SERVER, port=1883)
CLIENT.connect()

CLIENT.set_callback(custom_dispatcher)

# MQTT Topic subsciprtion
CLIENT.subscribe(MQTT_TOPIC_RED)
CLIENT.subscribe(MQTT_TOPIC_GREEN)
CLIENT.subscribe(MQTT_TOPIC_BLUE)
CLIENT.subscribe(MQTT_TOPIC_RGB)


# MQTT Check for new messages
def recieve_data(timer):
    CLIENT.check_msg()
    CLIENT.check_msg()
    CLIENT.check_msg()
    CLIENT.check_msg()


RECIEVE_DATA_TIMER = Timer(period=500, mode=Timer.PERIODIC, callback=recieve_data)


while True:
    pass
