import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt
import ssl
import signal
import sys

topic = "motors/control"

left_motor_pin = 7
right_motor_pin = 8
eje_motor_pin = 15
elevator_motor_pin = 16
led_right = 37
led_left = 35
camera_pin = 35
buzzer_pin = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(camera_pin, GPIO.OUT)

GPIO.setup(led_left, GPIO.OUT)
GPIO.setup(led_right, GPIO.OUT)

GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(left_motor_pin, GPIO.OUT)
GPIO.setup(right_motor_pin, GPIO.OUT)
GPIO.setup(eje_motor_pin, GPIO.OUT)
GPIO.setup(elevator_motor_pin, GPIO.OUT)

left_pwm = GPIO.PWM(left_motor_pin, 50)
right_pwm = GPIO.PWM(right_motor_pin, 50)
eje_pwm = GPIO.PWM(eje_motor_pin, 50)
elevator_pwm = GPIO.PWM(elevator_motor_pin, 50)
camera_pwm = GPIO.PWM(camera_pin, 50)

right_pwm.start(0)
left_pwm.start(0)
eje_pwm.start(0)
elevator_pwm.start(0)
camera_pwm.start(0)

adelante = 2.5
neutro = 0
atras = 12

camera_izquierda = 5
camera_derecha = 12

def elevator_up():
    eje_pwm.ChangeDutyCycle(adelante)
    sleep(1)
    eje_pwm.ChangeDutyCycle(neutro)
    sleep(1)
    elevator_pwm.ChangeDutyCycle(adelante)
    sleep(2)
    elevator_pwm.ChangeDutyCycle(neutro)
    
def elevator_down():
    elevator_pwm.ChangeDutyCycle(atras)
    sleep(2)
    elevator_pwm.ChangeDutyCycle(neutro)
    sleep(1)
    eje_pwm.ChangeDutyCycle(atras)
    sleep(1)
    eje_pwm.ChangeDutyCycle(neutro)

def go():
    stop()
    right_pwm.ChangeDutyCycle(adelante)
    left_pwm.ChangeDutyCycle(adelante)

def back():
    stop()
    right_pwm.ChangeDutyCycle(atras)
    left_pwm.ChangeDutyCycle(atras)

def left():
    stop()
    right_pwm.ChangeDutyCycle(adelante)
    left_pwm.ChangeDutyCycle(atras)

def right():
    stop()
    right_pwm.ChangeDutyCycle(atras)
    left_pwm.ChangeDutyCycle(adelante)
    
def stop():
    left_pwm.ChangeDutyCycle(neutro)
    right_pwm.ChangeDutyCycle(neutro)

def buzzer():
    GPIO.output(buzzer_pin, GPIO.LOW)
    GPIO.output(buzzer_pin, GPIO.HIGH)
    sleep(1)
    GPIO.output(buzzer_pin, GPIO.LOW)
    sleep(1)
    

def camera_left():
    camera_pwm.ChangeDutyCycle(camera_izquierda)
    sleep(1)
    camera_pwm.ChangeDutyCycle(neutro)
    
def camera_right():
    camera_pwm.ChangeDutyCycle(camera_derecha)
    sleep(1)
    camera_pwm.ChangeDutyCycle(neutro)

def turn_on_leds():
    GPIO.output(led_left, GPIO.HIGH)
    GPIO.output(led_right, GPIO.HIGH)

def turn_off_leds():
    GPIO.output(led_left, GPIO.LOW)
    GPIO.output(led_right, GPIO.LOW)
    
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado: " + str(rc))
    client.subscribe(topic)


"""
w -> para ir palante
a -> Para ir a la izquierda
s -> Para ir patra
d -> Para ir a la derechaj
e -> Para el Buzzer
i -> subir elevador
k -> bajar elevador
"""

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(payload)
    if payload == 'w':
        go()
    elif payload == 's':
        back()
    elif payload == 'd':
        right()
    elif payload == 'a':
        left()
    elif payload == 's':
        back()
    elif payload == 'i':
        elevator_up()
    elif payload == 'k':
        elevator_down()
    elif payload == 'x':
        stop()
    elif payload == 'e':
        buzzer()
    elif payload == 'o':
        camera_left()
    elif payload == 'p':
        camera_right()
    elif payload == 'l':
        turn_on_leds()
    elif payload == '2':
        turn_off_leds()
        

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


"""
lunes y martes prerevicon saber que es lo que va a faltas 22 y 23 revicion 
final pero si no se entrega el lunes y martes no se va a hacer la revicion 
se va directo a extra, tener lo mas listo posible este lunes y martes 
"""