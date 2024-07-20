import network
import simple
from machine import Timer
from RGB_Controller import RGB_Controller

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
CHECK_CONNECTION_TIMER = Timer(period=60000, mode=Timer.PERIODIC, callback=check_wifi_connection)

# MQTT Configuration

# MQTT Configuration
MQTT_SERVER = "broker.hivemq.com"
MQTT_CLIENT_NAME = "RGB-Controller-Malisevic"

MQTT_TOPIC_RED = b"RGB-Controller-Malisevic/red"
MQTT_TOPIC_GREEN = b"RGB-Controller-Malisevic/green"
MQTT_TOPIC_BLUE = b"RGB-Controller-Malisevic/blue"
MQTT_TOPIC_RGB = b"RGB-Controller-Malisevic/RGB_set"

def parse_rgb_string(rgb_bytes):
    # Decode the bytes object to a string
    rgb_string = rgb_bytes.decode('utf-8')
    
    # Extract the numeric values from the string
    rgb_values = rgb_string.split('(')[1].split(')')[0].split(',')
    
    # Convert the extracted values to integers
    r, g, b = [int(value.strip()) for value in rgb_values]
    
    # Scale the values to a range of 0 to 100
    r_scaled = (r / 255) * 100
    g_scaled = (g / 255) * 100
    b_scaled = (b / 255) * 100
    
    return r_scaled, g_scaled, b_scaled

# Example usage
rgb_string = b"rgb(86, 255, 0)"
r, g, b = parse_rgb_string(rgb_string)
print(r, g, b)

# MQTT Filtering recieved messages
def custom_dispatcher(topic, msg):
    global red_percent, green_percent, blue_percent

    if topic == MQTT_TOPIC_RED:
        red_percent = int(float(msg))
    elif topic == MQTT_TOPIC_GREEN:
        green_percent = int(float(msg))
    elif topic == MQTT_TOPIC_BLUE:
        blue_percent = int(float(msg))
    elif topic == MQTT_TOPIC_RGB:
        red_percent, green_percent, blue_percent = parse_rgb_string(msg)

    RGB_CONTROLLER.set_rgb_percent(red_percent, green_percent, blue_percent)


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
