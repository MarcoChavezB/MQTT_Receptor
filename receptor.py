import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt
import ssl
import signal
import sys

topic = "motors/control"

left_motor_pin = 7
right_motor_pin = 8
led_indicator_pin = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(left_motor_pin, GPIO.OUT)
GPIO.setup(right_motor_pin, GPIO.OUT)
GPIO.setup(led_indicator_pin, GPIO.OUT)

left_pwm = GPIO.PWM(left_motor_pin, 50)
right_pwm = GPIO.PWM(right_motor_pin, 50)
right_pwm.start(0)
left_pwm.start(0)

adelante = 2.5
neutro = 0
atras = 12

def go():
    stop()
    right_pwm.ChangeDutyCycle(adelante)
    left_pwm.ChangeDutyCycle(adelante)

def back():
    stop()
    right_pwm.ChangeDutyCycle(atras)
    left_pwm.ChangeDutyCycle(atras)

def stop():
    left_pwm.ChangeDutyCycle(neutro)
    right_pwm.ChangeDutyCycle(neutro)

def connected_led_indicator():
    GPIO.output(led_indicator_pin, GPIO.HIGH)

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado: " + str(rc))
    if rc == 0:
        connected_led_indicator()
    client.subscribe(topic)

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(payload)
    if payload == 'w':
        go()
    elif payload == 's':
        back()
    elif payload == 'd':
        stop()

def cleanup_gpio(signal, frame):
    print("\nLimpiando pines GPIO...")
    left_pwm.stop()
    right_pwm.stop()
    GPIO.cleanup()
    print("Pines GPIO limpiados correctamente.")
    sys.exit(0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(
    ca_certs='./AmazonRootCA1.pem',
    certfile='./cec69141d6f3a0869a78f2331a3b6acebf6bc9ddb27a738dc3945c2ea4a99618-certificate.pem.crt',
    keyfile='./cec69141d6f3a0869a78f2331a3b6acebf6bc9ddb27a738dc3945c2ea4a99618-private.pem.key',
    tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)

client.connect("a169mg5ru5h2z1-ats.iot.us-east-2.amazonaws.com", 8883, 60)

signal.signal(signal.SIGINT, cleanup_gpio)

client.loop_forever()
