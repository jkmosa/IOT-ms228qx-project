import network
import keys
from time import sleep
import machine
from umqtt.simple import MQTTClient
import os
import active_piezo
import RGB
from dht import DHT11

# Generate a unique MQTT client ID using random bytes
random_num = int.from_bytes(os.urandom(3), "little")  # changing the pseduo number to Integer.
mqtt_client_id = bytes("client_"+str(random_num), "utf-8")

# Adafruit IO server and credentials
ADAFRUIT_TO_URL = "io.adafruit.com"
ADAFRUIT_USERNAME = "jk_mosa"  # same username as my IG (if curious)
ADAFRUIT_TO_KEY = None  # replace with your adafruit API key

# Define MQTT feed topics
mqtt_humidity = "jk_mosa/feeds/humidity"
mqtt_temperature = "jk_mosa/feeds/temperature"
mqtt_buzzer = "jk_mosa/feeds/buzzer"
mqtt_light = "jk_mosa/feeds/light"
mqtt_fan = "jk_mosa/feeds/fan"

# input value for relay module on GPIO 16
relay_control_fan = machine.Pin(16, machine.Pin.OUT)

# Callback function to handle incoming MQTT messages


def sub_cb(topic, msg):
    topic = topic.decode("utf-8")
    msg = msg.decode("utf-8")

    if topic == mqtt_buzzer and msg == "ON":
        active_piezo.buzzer.value(1)
        print("buzzer turned on")

    if topic == mqtt_buzzer and msg == "OFF":
        active_piezo.buzzer.value(0)
        print("buzzer turned off")

    if topic == mqtt_light and msg == "ON":
        RGB.LED_Pin_Red.value(1)
        print("light turned on")

    if topic == mqtt_light and msg == "OFF":
        RGB.LED_Pin_Red.value(0)
        print("light turned off")

    if topic == mqtt_fan and msg == "ON":
        relay_control_fan.value(1)
        print("fan turned on")

    if topic == mqtt_fan and msg == "OFF":
        relay_control_fan.value(0)
        print("fan turned off")

# Connect to Wi-Fi using credentials from keys.py


def connect():
    # WiFi Connection
    wlan = network.WLAN(network.STA_IF)  # Put modem on Station mode
    wlan.active(True)
    wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)  # pass SSID and PASSCODE as an argument.

    while not wlan.isconnected():
        sleep(3)
        # print(wlan.scan())
        print(wlan.isconnected())
        print("waiting for connection...")

    print("connected to wifi.")
    # print(wlan.ifconfig())


connect()

# Connect to Adafruit IO MQTT broker


def mqtt_connect():
    client = MQTTClient(client_id=mqtt_client_id,
                        server=ADAFRUIT_TO_URL,
                        user=ADAFRUIT_USERNAME,
                        password=ADAFRUIT_TO_KEY,
                        ssl=False)
    client.connect()
    print("Connected to adafruit MQTT broker.")
    return client

# If MQTT connection fails, wait and reset the device


def reconnect():
    print("Failed to connect MQTT Broker. Reconnecting...")
    RGB.LED_Pin_Blue.value(1)
    sleep(5)
    RGB.LED_Pin_Blue.value(0)
    machine.reset()

# Try to connect to the broker, or reset if it fails


try:
    client = mqtt_connect()
    RGB.LED_Pin_Green.value(1)
    sleep(1.5)
    RGB.LED_Pin_Green.value(0)


except OSError:
    reconnect()


client.set_callback(sub_cb)  # Set the callback function

# subscribe to topics
client.subscribe(mqtt_buzzer)
client.subscribe(mqtt_light)
client.subscribe(mqtt_fan)


# Initialize DHT11 temperature and humidity sensor on GPIO 27
tempSensor = DHT11(machine.Pin(27))

try:
    while True:
        client.check_msg()  # Check for new MQTT messages
        try:
            # Read temperature and humidity from sensor
            tempSensor.measure()
            temperature = tempSensor.temperature()
            humidity = tempSensor.humidity()
            client.check_msg()

            # If humidity is too low
            if humidity <= 30:
                print("Low humidity detected!")
                RGB.LED_Pin_Red.value(1)
                active_piezo.buzzer.value(1)
                sleep(1)
                RGB.LED_Pin_Red.value(0)
                active_piezo.buzzer.value(0)

            # If humidity is too high
            elif humidity >= 50:
                print("High humidity detected!")
                RGB.LED_Pin_Red.value(1)
                active_piezo.buzzer.value(1)
                sleep(1)
                RGB.LED_Pin_Red.value(0)
                active_piezo.buzzer.value(0)

            else:
                print("Humidity is normal.")

            # Publish data to Adafruit IO
            client.publish(mqtt_humidity, str(humidity), qos=0)
            client.publish(mqtt_temperature, str(temperature), qos=0)
            print("Temperature: {}°C, Humidity: {}%".format(temperature, humidity))
            client.check_msg()
            sleep(5)

        except Exception as error:
            print("Exception occurred", error)

        sleep(0.5)

finally:
    # Clean up: turn off buzzer and LEDs
    active_piezo.buzzer.value(0)
    RGB.LED_Pin_Blue.value(0)
    RGB.LED_Pin_Red.value(0)
    RGB.LED_Pin_Green.value(0)
    # relay_control_fan.value(0) not realy important since the relay module is setup in normaly closed terminal
    print("Program stopped. All alerts turned off.")
