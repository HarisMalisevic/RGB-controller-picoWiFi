import network
import simple
from machine import Timer
from RGB_Controller import RGB_Controller

# RGB Controller Setup
RGB_CONTROLLER = RGB_Controller(17, 16, 19)


# WiFi configuration
WIFI_SSID = "Malisevic"
WIFI_PASSWORD = "Ari_bjelov"

#Connecting to WiFi
print("Connecting to WiFi: ", WIFI_SSID)
WIFI = network.WLAN(network.STA_IF)
WIFI.active(True)
WIFI.config(pm=0xA11140)
WIFI.connect(WIFI_SSID, WIFI_PASSWORD)

while not WIFI.isconnected():
    pass

print("Connected to network!")
print("IP address:", WIFI.ifconfig()[0])

# MQTT Configuration

# MQTT Configuration
MQTT_SERVER = "broker.hivemq.com"
MQTT_CLIENT_NAME = "RGB-Controller-Malisevic"

MQTT_TOPIC_RED = b"RGB-Controller-Malisevic/red"
MQTT_TOPIC_GREEN = b"RGB-Controller-Malisevic/green"
MQTT_TOPIC_BLUE = b"RGB-Controller-Malisevic/blue"

# MQTT Filtering recieved messages
def custom_dispatcher(topic, msg):

    if topic == MQTT_TOPIC_RED:
        RGB_CONTROLLER.red.duty_u16(int(float(msg))) 
    elif topic == MQTT_TOPIC_GREEN:
        RGB_CONTROLLER.green.duty_u16(int(float(msg))) 
    elif topic == MQTT_TOPIC_BLUE:
        RGB_CONTROLLER.blue.duty_u16(int(float(msg))) 

# MQTT Connecting to broker
CLIENT = simple.MQTTClient(client_id=MQTT_CLIENT_NAME, server=MQTT_SERVER, port=1883)
CLIENT.connect()

CLIENT.set_callback(custom_dispatcher)

# MQTT Topic subsciprtion
CLIENT.subscribe(MQTT_TOPIC_RED)
CLIENT.subscribe(MQTT_TOPIC_GREEN)
CLIENT.subscribe(MQTT_TOPIC_BLUE)

# MQTT Check for new messages
def recieve_data(timer):
    CLIENT.check_msg()
    CLIENT.check_msg()
    CLIENT.check_msg()

RECIEVE_DATA_TIMER = Timer(period=500, mode=Timer.PERIODIC, callback=recieve_data)


while True:
    pass
