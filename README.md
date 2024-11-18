# How to use:

1. After cloning, set these parameters in config.json:
{
    "WIFI_SSID": "ssid",
    "WIFI_PASSWORD": "password",

    "MQTT_CLIENT_NAME": "RGB-Controller",
    "MQTT_SERVER": "192.168.1.12",
    
    "MQTT_TOPIC_GREEN": "RGB-Controller/green",
    "MQTT_TOPIC_BLUE": "RGB-Controller/blue",
    "MQTT_TOPIC_RGB": "RGB-Controller/RGB_set",
    "MQTT_TOPIC_RED": "RGB-Controller/red"
}

2. Copy all files to Pico W - main.py will autorun on reboot
