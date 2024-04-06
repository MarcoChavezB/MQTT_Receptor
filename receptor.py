import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt
import ssl

topic="motors/control"

# Configuración de los pines de los motores
left_motor_pin = 11
right_motor_pin = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(left_motor_pin, GPIO.OUT)
GPIO.setup(right_motor_pin, GPIO.OUT)

left_pwm = GPIO.PWM(left_motor_pin, 50)
right_pwm = GPIO.PWM(right_motor_pin, 50)
right_pwm.start(0)
left_pwm.start(0)

# Configuración de los valores de ciclo de trabajo %
adelante = 2.5
neutro = 7.5
atras = 12

# Funciones para controlar los motores
def go():
    right_pwm.ChangeDutyCycle(adelante)
    left_pwm.ChangeDutyCycle(adelante)

def back():
    left_pwm.ChangeDutyCycle(atras)
    right_pwm.ChangeDutyCycle(atras)

def stop():
    left_pwm.ChangeDutyCycle(neutro)
    right_pwm.ChangeDutyCycle(neutro)

# Función de conexión MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado: " + str(rc))
    client.subscribe(topic)

# Función para procesar los mensajes MQTT
def on_message(self, client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print(message)
    if message == 'w':
        go()
    elif message == 's':
        back()
    elif message == ' ':
        stop()

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Configuración TLS
client.tls_set(
    ca_certs='./AmazonRootCA1.pem', 
    certfile='./cec69141d6f3a0869a78f2331a3b6acebf6bc9ddb27a738dc3945c2ea4a99618-certificate.pem.crt', 
    keyfile='./cec69141d6f3a0869a78f2331a3b6acebf6bc9ddb27a738dc3945c2ea4a99618-private.pem.key', 
    tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)

# Conexión al broker MQTT
client.connect("a169mg5ru5h2z1-ats.iot.us-east-2.amazonaws.com", 8883, 60)

# Loop principal del cliente MQTT
client.loop_forever()
