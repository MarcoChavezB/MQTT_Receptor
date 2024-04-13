import serial
import paho.mqtt.client as mqtt
import ssl
import signal
import sys

topic = "motors/control"


ser = serial.Serial('/dev/ttyUSB0', 9600) 

def send_command(command):
    ser.write(command.encode())

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado: " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(payload)
    send_command(payload)

def cleanup_serial(signal, frame):
    print("\nCerrando conexión serial...")
    ser.close()
    print("Conexión serial cerrada correctamente.")
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

signal.signal(signal.SIGINT, cleanup_serial)

client.loop_forever()
