from machine import Pin, PWM
import time

buzzer = Pin(14, Pin.OUT)  # setting Pin 14 to output to active buzzer

# buzzer = PWM(Pin(14))
# buzzer.freq(500)
# buzzer.duty_u16(800)

if __name__ == "__main__":

    try:
        while True:
            buzzer.value(1)
            print("Buzzer active...")
            time.sleep(2)
            buzzer.value(0)
            print("Buzzer active...")
            time.sleep(2)

    finally:
        buzzer.value(0)  # Ensure buzzer is turned off on stop
        print("Program stopped, buzzer turned off.")
