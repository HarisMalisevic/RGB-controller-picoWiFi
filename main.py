import network
import simple
from machine import Timer
from RGB_Controller import RGB_Controller

import json
import os

CONFIG_FILE_NAME = "config.json"
U_16 = 2**16 - 1

# Configuration variables
WIFI_SSID = ""
WIFI_PASSWORD = ""

MQTT_SERVER = ""
MQTT_CLIENT_NAME = ""

MQTT_TOPIC_RED = b""
MQTT_TOPIC_GREEN = b""
MQTT_TOPIC_BLUE = b""
MQTT_TOPIC_RGB = b""


# Save configuration variables to JSON file
def save_config():
    config = {
        "WIFI_SSID": WIFI_SSID,
        "WIFI_PASSWORD": WIFI_PASSWORD,
        "MQTT_SERVER": MQTT_SERVER,
        "MQTT_CLIENT_NAME": MQTT_CLIENT_NAME,
        "MQTT_TOPIC_RED": MQTT_TOPIC_RED.decode("utf-8"),
        "MQTT_TOPIC_GREEN": MQTT_TOPIC_GREEN.decode("utf-8"),
        "MQTT_TOPIC_BLUE": MQTT_TOPIC_BLUE.decode("utf-8"),
        "MQTT_TOPIC_RGB": MQTT_TOPIC_RGB.decode("utf-8"),
    }

    with open(CONFIG_FILE_NAME, "w") as file:
        file.write(json.dumps(config))

    print(f"Configuration saved to file: {config}")

# Load configuration variables from JSON file
def load_config():
    global WIFI_SSID, WIFI_PASSWORD, MQTT_SERVER, MQTT_CLIENT_NAME, MQTT_TOPIC_RED, MQTT_TOPIC_GREEN, MQTT_TOPIC_BLUE, MQTT_TOPIC_RGB

    if not CONFIG_FILE_NAME in os.listdir():
        print("No configuration file found!")
        exit()

    with open(CONFIG_FILE_NAME, "r") as file:
        config = json.load(file)

    WIFI_SSID = config.get("WIFI_SSID")
    WIFI_PASSWORD = config.get("WIFI_PASSWORD")
    MQTT_SERVER = config.get("MQTT_SERVER")
    MQTT_CLIENT_NAME = config.get("MQTT_CLIENT_NAME")
    MQTT_TOPIC_RED = config.get("MQTT_TOPIC_RED").encode("utf-8")
    MQTT_TOPIC_GREEN = config.get("MQTT_TOPIC_GREEN").encode("utf-8")
    MQTT_TOPIC_BLUE = config.get("MQTT_TOPIC_BLUE").encode("utf-8")
    MQTT_TOPIC_RGB = config.get("MQTT_TOPIC_RGB").encode("utf-8")

    print(f"Configuration loaded from file: {CONFIG_FILE_NAME}")


load_config()

# RGB Controller Setup
RGB_CONTROLLER = RGB_Controller(17, 16, 19)


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
