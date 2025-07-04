# IOT-ms228qx-project
humidity sensor
# IOT project report 

Mussie Assefa (ms228qx)

## Introduction 

A humidity sensor continuously monitors the surrounding air and detects abnormal humidity levels. When high or low humidity is detected, the system responds by triggering a buzzer (audible alert) and flashing an LED (visual alert). This allows individuals especially sinusitis patients to take timely action, such as turning on a dehumidifier or opening a window, helping to alleviate their symptoms and prevent further discomfort.

This project can be realistically completed within a week, provided the components (sensors, GPIO, and SPI communication protocols) are understood at a basic level.

## Objective

I chose the humidity sensor based on personal needs, as I often experience a runny nose when humidity levels are too high. By monitoring and collecting humidity data, I can better manage indoor air quality. Specifically, when the humidity drops below 30% or rises above 50%, the system can trigger alerts, allowing for timely actions such as using a dehumidifier or improving ventilation.

Additionally, the collected data can be used for statistical analysis, contributing to improved environmental control over time and potentially benefiting others with similar sensitivities.

## Material 

I bought all this bellow items (not including dht11 sensor) and other included spares from ***Freenova*** an electronic kit package vendor which costed around SEK 350. The dht11 sensor was bought from ***Electrokit*** which costed around SEK 50.

>List of material used:
- **Raspberry pi pico w** :- is a microcontroler which sets an instruction to sensor out to GPIO 14 for the active piezo buzzer, GPIO 10 and 15 to Blue light and red light respectively and GPIO 27 to dht11 sensor powering it using pin 3v3 (3 volts).

![Screenshot 2025-07-03 130448](https://hackmd.io/_uploads/H1wcLk4Sgl.png)

- **Jumper wire** :- they are wires used to connect sensors to microcontroler through a breadboared.

![Screenshot 2025-07-03 130804](https://hackmd.io/_uploads/SyJ5_1Nrgg.png)


- **Bread boared** :- is a media of interface which is used for a simplification of wire connection and clean look for the design.

![Screenshot 2025-07-03 130417](https://hackmd.io/_uploads/HJjI1eErxx.png)


- **Dht11 sensor** :- The sensor measures humidity and temperature every 3 seconds via the instruction of the microcontroler using Micropython.

![Screenshot 2025-07-03 135427](https://hackmd.io/_uploads/HkRFkl4Bge.png)


- **LED light** :- Thier are two anode light Blue and Red where Red is incorporated with disconnected network signal and blue gives a warning singal when the humidity pass the maximum threshold or it's below the minimum threshold in sensors surrounding. 

![Screenshot 2025-07-03 125516](https://hackmd.io/_uploads/S1lnygNSxe.png)


- **Active piezo buzzer** :- sound is activated when the humidity pass the maximum threshold or it's below the minimum threshold in sensors surrounding.

![Screenshot 2025-07-03 123740](https://hackmd.io/_uploads/BJ-1glEBle.png)

## Computer setup

The device was programmed using Thonny IDE, which is beginner-friendly and comes with built-in support for MicroPython—no extra packages required. Its clean interface avoids the complexity of IDEs like VS Code, making it ideal for new users.

The MicroPython firmware was flashed onto the Raspberry Pi Pico using a .uf2 file downloaded from the official MicroPython website. This file format, developed by Microsoft's MakeCode team, makes it easy to drag and drop firmware onto the device.

The MicroPython interpreter was selected in Thonny by navigating to Tools → Options → Interpreter, and choosing either MicroPython (Raspberry Pi Pico) or MicroPython (RP2040).

The code was uploaded to GitHub for version control and sharing. Alternatively, platforms like HackMD can be used for collaborative documentation.


## putting everything togeather


## plateform 

I used Adafruit a cloud service which is Saas where the core functionality of Adafruit is Data Storage Storing incoming data from sensors/devices like:-
- Temperature
- Humidity
- Button presses for light and buzzer

Each data stream is stored in a feed, which acts like a time series log. For the project a free tier was efficent.

Adafruit IO is known for being easy to set up, with clear documentation and examples that are especially friendly to:
- Students
- Hobbyists
- IoT beginners

This allowed me to get started quickly without deep experience in cloud platforms or IoT protocols. Adafruit IO allows you to create interactive dashboards where you can:

- Visualize sensor data (e.g., temperature, humidity)
- Use toggles, sliders, and buttons to send commands back to devices

This bi-directional control made it ideal for projects like humidity sensor. Scaling my idea using Adafruit has a seamless obstacle.


## The code

![Screenshot 2025-07-03 212331](https://hackmd.io/_uploads/BJmkFU4Hex.png)

The tempSensor is an instance of the DHT11 class, connected to GPIO pin 27. It collects environmental data using the measure() function, which retrieves both temperature and humidity readings from the sensor.

>The logic includes two conditional checks based on humidity levels:

- If the humidity falls below 30%, both the LED and the buzzer are activated for one second, then turned off.
- If the humidity rises above 50%, the same alert pattern occurs—LED and buzzer turn on for one second, then off.
- For humidity levels between 30% and 50%, no alert is triggered; the system continues to monitor silently.

Regardless of the alert status, the program publishes humidity and temperature data every 5 seconds to Adafruit IO using the MQTT protocol over a Wi-Fi connection.

## Transmitting the data / connectivity

The project uses **Wi-Fi** as the wireless protocol and **MQTT** as the transport protocol. Wi-Fi is built into the Raspberry Pi Pico W, making it a convenient and reliable choice for connecting the device to the internet without requiring additional hardware, offering good range for indoor environments but with moderate power consumption. It offers stable, high-speed connectivity suitable for real-time data transmission. For transport, MQTT (Message Queuing Telemetry Transport) is used due to its lightweight nature, low bandwidth usage, reducing data size and battery usage, and efficient publish/subscribe model. This makes it ideal for IoT applications like this one, where sensor data (temperature and humidity) needs to be sent periodically to a cloud server (Adafruit IO) over a Wi-Fi connection.

## Presenting the data

In this project, data is sent to Adafruit IO every 5 seconds using the client.publish() function in a loop. Each publish operation sends temperature and humidity readings to their respective feeds (topics), and Adafruit IO automatically saves each received data point in its cloud database. So effectively, data is saved every 5 seconds, assuming a stable Wi-Fi and MQTT connection.

Automation and triggers in this project are handled via MQTT subscriptions to specific topics. When the device receives messages like "ON" or "OFF" on the buzzer or light MQTT feeds, callback functions activate or deactivate the buzzer and LEDs accordingly. Additionally, the device itself triggers alerts automatically based on sensor readings—if humidity falls below 30% or rises above 50%, it turns on the buzzer and LED for a short period. This combination of sensor-driven triggers and remote MQTT commands enables both automatic responses and user-controlled actions.

## Finalizing the design